# populate_db.py
import sqlite3
import pandas as pd
from pathlib import Path

DB = "foodwaste.db"

def run_sql_file(conn, path):
    sql = Path(path).read_text()
    conn.executescript(sql)

def create_db():
    conn = sqlite3.connect(DB)
    run_sql_file(conn, "schema.sql")
    conn.commit()
    return conn

def insert_sample(conn):
    cur = conn.cursor()
    # sample providers
    cur.execute("INSERT INTO Providers (Name, Provider_Type, Contact, Address) VALUES (?, ?, ?, ?)",
                ("Spice Corner", "Restaurant", "9876543210", "Sector 10, Ranchi"))
    provider_id = cur.lastrowid
    # sample listing
    cur.execute("""INSERT INTO Food_Listings (Food_Name, Quantity, Unit, Location, Expiry_Date, Provider_ID, Provider_Type, Contact, Notes)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                ("Vegetable Biryani", 20, "packs", "Ranchi", "2025-08-15", provider_id, "Restaurant", "9876543210", "Leftover banquet"))
    conn.commit()

def ingest_csvs(conn):
    # If you have CSVs in data/, load them automatically
    d = Path("data")
    if (d / "providers.csv").exists():
        df = pd.read_csv(d / "providers.csv")
        df.to_sql("Providers", conn, if_exists="append", index=False)
    if (d / "food_listings.csv").exists():
        df = pd.read_csv(d / "food_listings.csv")
        df.to_sql("Food_Listings", conn, if_exists="append", index=False)

if __name__ == "__main__":
    conn = create_db()
    ingest_csvs(conn)
    insert_sample(conn)
    conn.close()
    print("DB created and sample data inserted into foodwaste.db")
