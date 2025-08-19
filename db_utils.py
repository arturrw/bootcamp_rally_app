import snowflake.connector
import pandas as pd
import os

def get_connection():
    """Connecting to Snowflake"""
    conn = snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
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
