FROM python:3.11-slim AS base 

FROM base AS builder
COPY --from=ghcr.io/astral-sh/uv:0.5.14 /uv /usr/local/bin/uv

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1

WORKDIR /app

COPY pyproject.toml /app/
COPY uv.lock /app/
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev -vv



COPY datagen/firehose.py /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev -vv

FROM base 
COPY --from=builder /app /app
ENV PATH="/app/.venv/bin:$PATH"

CMD ["python","/app/firehose.py"]
