from pyspark.sql import SparkSession

def main():
    spark = (
        SparkSession.builder
        .appName("CSV_to_Iceberg_Python")
        # Iceberg catalog, метаданные в Hive Metastore
        .config("spark.sql.catalog.demo", "org.apache.iceberg.spark.SparkCatalog")
        .config("spark.sql.catalog.demo.type", "hive")
        .config("spark.sql.catalog.demo.uri", "thrift://hive-metastore:9083")
        .config("spark.sql.catalog.demo.warehouse", "s3a://warehouse/")
        # S3/MinIO
        .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000")
        .config("spark.hadoop.fs.s3a.access.key", "minio")
        .config("spark.hadoop.fs.s3a.secret.key", "minio123")
        .config("spark.hadoop.fs.s3a.path.style.access", "true")
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .enableHiveSupport()
        .getOrCreate()
    )

    csv_path = "/data/input_wide.csv"
    df = spark.read.option("header", "true").csv(csv_path)

    df.writeTo("demo.csv_wide_py").using("iceberg").createOrReplace()

    print("Written CSV -> Iceberg (demo.csv_wide_py)")
    spark.stop()

if __name__ == "__main__":
    main()
