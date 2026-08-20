# Drug Adverse Events Data Pipeline

## What It Does
Pulls drug adverse event reports from the openFDA API and loads them into PostgreSQL.

## Tech Stack
Python, Pandas, SQLAlchemy, Docker, Docker Compose, PostgreSQL, UV, Click

## How To Run

1. Start the database:
docker compose up -d

2. Build the pipeline:
docker build -t adverse-events:pipeline .

3. Run the ingestion:
docker run --rm --network api_work_default adverse-events:pipeline --pg_host pg-database

4. Verify in PG Admin:
Open localhost:8085 (admin@admin.com / root)

## Data Source
openFDA Drug Adverse Event API (https://api.fda.gov/drug/event.json)

## Data Fields
- report_id, receive_date, serious, seriousnessdeath
- patient_age, patient_sex, drug_name, reaction, country