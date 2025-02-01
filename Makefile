up:
	docker compose up -d --build 
down:
	docker compose down -v --volumes --remove-orphans

restart: down up

submit:
	docker exec -d firehose-spark-master spark-submit --master spark://spark-master:7077 --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.3,org.apache.hadoop:hadoop-aws:3.3.3 --deploy-mode client ./apps/batchstream.py