FROM apache/spark:3.4.4-python3 as base

FROM base AS builder
COPY --from=ghcr.io/astral-sh/uv:0.5.14 /uv /usr/local/bin/uv
USER root
ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1

WORKDIR /app

COPY pyproject.toml /app/
COPY uv.lock /app/
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev -vv



COPY connect/batchstream.py /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev -vv

FROM base 
COPY --from=builder /app /app
ENV PATH="/app/.venv/bin:$PATH"


# RUN wget https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/3.5.1/spark-sql-kafka-0-10_2.12-3.5.1.jar -o /app/spark-sql-kafka-0-10_2.12-3.5.1.jar
# RUN wget https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.4.1/hadoop-aws-3.4.1.jar -o /app/hadoop-aws-3.4.1.jar


CMD ["spark-submit","--packages","org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.4,org.apache.hadoop:hadoop-aws:3.4.4","/app/batchstream.py"]

