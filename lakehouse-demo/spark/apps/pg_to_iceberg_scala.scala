import org.apache.spark.sql.SparkSession
import java.util.Properties

object PgToIcebergScala {
  def main(args: Array[String]): Unit = {
    val spark = SparkSession.builder()
      .appName("PG_to_Iceberg_Scala")
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

    val jdbcUrl = "jdbc:postgresql://pg_source:5432/demo_db"
    val props = new Properties()
    props.setProperty("user", "demo")
    props.setProperty("password", "demo")
    props.setProperty("driver", "org.postgresql.Driver")

    val df = spark.read.jdbc(jdbcUrl, "wide_table", props)

    df.writeTo("demo.pg_wide_scala").using("iceberg").createOrReplace()

    println("Written Postgres -> Iceberg (demo.pg_wide_scala)")
    spark.stop()
  }
}
