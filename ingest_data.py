#!/usr/bin/env python
# coding: utf-8

import argparse
import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm


def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    dtype = {
        "VendorID": "Int64",
        "passenger_count": "Int64",
        "trip_distance": "float64",
        "RatecodeID": "Int64",
        "store_and_fwd_flag": "string",
        "PULocationID": "Int64",
        "DOLocationID": "Int64",
        "payment_type": "Int64",
        "fare_amount": "float64",
        "extra": "float64",
        "mta_tax": "float64",
        "tip_amount": "float64",
        "tolls_amount": "float64",
        "improvement_surcharge": "float64",
        "total_amount": "float64",
        "congestion_surcharge": "float64",
    }

    parse_dates = ["tpep_pickup_datetime", "tpep_dropoff_datetime"]

    engine = create_engine(
        f"postgresql+psycopg://{user}:{password}@{host}:{port}/{db}"
    )

    print("Conectando e iniciando a leitura da URL...")

    # O pandas baixa e faz o stream do arquivo .csv.gz via HTTP nativamente
    df_iter = pd.read_csv(
        url,
        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=100000,
    )

    first = True
    for df_chunk in tqdm(df_iter):
        if first:
            df_chunk.head(0).to_sql(
                name=table_name, con=engine, if_exists="replace"
            )
            first = False
            print("Tabela criada no banco de dados.")

        df_chunk.to_sql(name=table_name, con=engine, if_exists="append")
        print("Inserido bloco de tamanho:", len(df_chunk))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Ingest CSV data to PostgreSQL"
    )

    parser.add_argument("--user", required=True, help="user name for postgres")
    parser.add_argument(
        "--password", required=True, help="password for postgres"
    )
    parser.add_argument("--host", required=True, help="host for postgres")
    parser.add_argument("--port", required=True, help="port for postgres")
    parser.add_argument(
        "--db", required=True, help="database name for postgres"
    )
    parser.add_argument(
        "--table_name",
        required=True,
        help="name of the table where we will write the results to",
    )
    parser.add_argument("--url", required=True, help="url of the csv file")

    args = parser.parse_args()
    main(args)