# About
This repo contains necessary codes to fetch from Bluesky's firestream websocket and sends the data to Kafka

# How to run
Run `docker compose up -d` to set-up Kafka & Zookeeper. After Kafka is up and running run `python datagen/firehose.py` to start pushing data to Kafka. 

Then run `python connect/batchstream.py` to launch a pyspark job that connects to Kafka & writes the data to a parquet file, partitioning by date & hour.