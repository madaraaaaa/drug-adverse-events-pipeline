FROM python:3.13.1-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /code

COPY pyproject.toml uv.lock .python-version ./
RUN uv sync --locked

COPY ingest.py .

ENV PATH="/code/.venv/bin:$PATH"

ENTRYPOINT ["python", "ingest.py"]