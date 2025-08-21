# db.py
import sqlite3
import pandas as pd
import streamlit as st

DB_PATH = "foodwaste.db"

@st.cache_resource
def get_conn(path=DB_PATH):
    conn = sqlite3.connect(path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def run_query(sql, params=None):
    conn = get_conn()
    return pd.read_sql_query(sql, conn, params=params or [])

def execute(sql, params=None):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(sql, params or [])
    conn.commit()
    return cur
