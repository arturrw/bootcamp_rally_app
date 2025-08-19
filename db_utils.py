import snowflake.connector
import pandas as pd
import os

def get_connection():
    """Connecting to Snowflake"""
    conn = snowflake.connector.connect(
        user=os.getenv("ARTURSMINOVS"),
        password=os.getenv("Zaqwsxcderfvbgty!26"),
        account=os.getenv("hu01507.eu-north-1.aws"),
        warehouse=os.getenv("BOOTCAMP_WH"),
        database="BOOTCAMP_RALLY",
        schema="RALLY_SCHEMA"
    )
    return conn

def fetch_df(query):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query)
    df = cur.fetch_pandas_all()
    cur.close()
    conn.close()
    return df

def execute(query, params=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params)
    conn.commit()
    cur.close()
    conn.close()

