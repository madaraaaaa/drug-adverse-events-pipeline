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

## Orchestration (Kestra)

This pipeline is orchestrated using Kestra with a staging + merge pattern to avoid duplicate records on repeated runs.

**Flow:** `flows/drug_adverse_events_pipeline.yaml`

**Pipeline steps:**
1. Create final table (if not exists)
2. Create and truncate staging table
3. Extract records from openFDA API and load into staging
4. Merge only new records (by `report_id`) from staging into final table
5. Clean up staging table

**Schedule:** Runs automatically every Monday at 6am (currently disabled for testing — enable in the trigger section)

**To run:**
1. `docker compose up -d`
2. Open `localhost:8080`
3. Create a new flow and paste `flows/drug_adverse_events_pipeline.yaml`
4. Execute manually, or enable the trigger for automatic weekly runs