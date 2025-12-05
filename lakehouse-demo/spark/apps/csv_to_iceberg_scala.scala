import org.apache.spark.sql.SparkSession

object CsvToIcebergScala {
  def main(args: Array[String]): Unit = {
    val spark = SparkSession.builder()
      .appName("CSV_to_Iceberg_Scala")
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

    val df = spark.read
      .option("header", "true")
      .csv("/data/input_wide.csv")

    df.writeTo("demo.csv_wide_scala").using("iceberg").createOrReplace()

    println("Written CSV -> Iceberg (demo.csv_wide_scala)")
    spark.stop()
  }
}
