FROM bitnami/spark:3.5.1

USER root

# Путь для JAR'ов
ENV SPARK_HOME=/opt/bitnami/spark

# Скопируем конфиги Hadoop/S3
COPY ../hadoop/core-site.xml /opt/bitnami/spark/conf/core-site.xml
COPY ../hadoop/hdfs-site.xml /opt/bitnami/spark/conf/hdfs-site.xml

# JAR'ы для Iceberg + S3 (версии можешь подправить под свои)
# Можно скачать вручную и положить в spark/jars, а тут только скопировать
COPY jars/* ${SPARK_HOME}/jars/

# Приложения
COPY apps/ ${SPARK_HOME}/apps/

# Python зависимости (если нужны)
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt || true

USER 1001
