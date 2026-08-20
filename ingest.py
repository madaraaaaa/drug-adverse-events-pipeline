import requests
import pandas as pd
from sqlalchemy import create_engine
from tqdm import tqdm
import click

def flatten_event(event):
    return {
        "report_id": event.get('safetyreportid'),
        "receive_date": pd.to_datetime(event.get('receivedate'), format="%Y%m%d", errors="coerce"),
        "serious": event.get('serious') == "1",
        "seriousnessdeath": event.get('seriousnessdeath'),
        "patient_age": pd.to_numeric(event.get('patient', {}).get('patientonsetage'), errors="coerce"),
        "patient_sex": {"1": "Male", "2": "Female"}.get(event.get('patient', {}).get('patientsex')),
        "drug_name": event.get('patient', {}).get('drug', [{}])[0].get('medicinalproduct'),
        "reaction": event.get('patient', {}).get('reaction', [{}])[0].get('reactionmeddrapt'),
        "country": event.get('primarysource', {}).get('reportercountry'),
    }

@click.command()
@click.option("--pg_user", default="root")
@click.option("--pg_password", default="root")
@click.option("--pg_host", default="localhost")
@click.option("--pg_port", default="5432")
@click.option("--pg_db", default="adverse_events")
@click.option("--table_name", default="raw_adverse_events")
@click.option("--total_records", default=10000)
@click.option("--batch_size", default=100)
def main(pg_user, pg_password, pg_host, pg_port, pg_db, table_name, total_records, batch_size):
    engine = create_engine(f"postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}")

    first = True

    for skip in tqdm(range(0, total_records, batch_size)):
        url = f"https://api.fda.gov/drug/event.json?limit={batch_size}&skip={skip}"
        response = requests.get(url)
        rows = [flatten_event(e) for e in response.json()["results"]]
        df = pd.DataFrame(rows)
        
        if first:
            df.to_sql(table_name, engine, if_exists="replace", index=False)
            first = False
        else:
            df.to_sql(table_name, engine, if_exists="append", index=False)

    print(f"Done. Inserted {total_records} records into {table_name}")

if __name__ == "__main__":
    main()