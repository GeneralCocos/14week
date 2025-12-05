from pyspark.sql import SparkSession

def main():
    spark = (
        SparkSession.builder
        .appName("PG_to_Iceberg_Python")
        .config("spark.sql.catalog.demo", "org.apache.iceberg.spark.SparkCatalog")
        .config("spark.sql.catalog.demo.type", "hive")
        .config("spark.sql.catalog.demo.uri", "thrift://hive-metastore:9083")
        .config("spark.sql.catalog.demo.warehouse", "s3a://warehouse/")
        .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000")
        .config("spark.hadoop.fs.s3a.access.key", "minio")
        .config("spark.hadoop.fs.s3a.secret.key", "minio123")
        .config("spark.hadoop.fs.s3a.path.style.access", "true")
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .enableHiveSupport()
        .getOrCreate()
    )

    jdbc_url = "jdbc:postgresql://pg_source:5432/demo_db"
    props = {
        "user": "demo",
        "password": "demo",
        "driver": "org.postgresql.Driver"
    }

    df = spark.read.jdbc(jdbc_url, "wide_table", properties=props)

    df.writeTo("demo.pg_wide_py").using("iceberg").createOrReplace()

    print("Written Postgres -> Iceberg (demo.pg_wide_py)")
    spark.stop()

if __name__ == "__main__":
    main()
