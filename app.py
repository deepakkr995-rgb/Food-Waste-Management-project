import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# ==========================
# DB CONNECTION
# ==========================
DB_FILE = "foodwaste.db"

def run_query(query, params=()):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(query, params)
    rows = cur.fetchall()
    cols = [description[0] for description in cur.description]
    conn.close()
    return pd.DataFrame(rows, columns=cols)

def run_execute(query, params=()):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(query, params)
    conn.commit()
    conn.close()

# ==========================
# STREAMLIT APP
# ==========================
st.set_page_config(page_title="Food Waste Management", layout="wide")

st.sidebar.title("Navigation")
choice = st.sidebar.radio(
    "Go to",
    [
        "Project Introduction",
        "View Tables",
        "CRUD Operations",
        "SQL Queries & Visualization",
        "Learner SQL Queries",
        "User Introduction"
    ]
)

# ==========================
# 1. PROJECT INTRODUCTION
# ==========================
if choice == "Project Introduction":
    st.title("🌍 Local Food Wastage Management System")
    st.markdown("""
    This project helps manage surplus food and reduce wastage by connecting providers with those in need.

    - **Providers** 🍴: Restaurants, households, and businesses list surplus food.  
    - **Receivers** 🏡: NGOs and individuals claim available food.  
    - **Geolocation** 📍: Helps locate nearby food.  
    - **SQL Analysis** 📊: Powerful insights using SQL queries.  
    """)

# ==========================
# 2. VIEW TABLES
# ==========================
elif choice == "View Tables":
    st.title("📂 View Database Tables")
    table = st.selectbox("Choose a table", ["Providers", "Receivers", "Food_Listings", "Claims"])
    df = run_query(f"SELECT * FROM {table}")
    st.dataframe(df, use_container_width=True)

# ==========================
# 3. CRUD OPERATIONS
# ==========================
elif choice == "CRUD Operations":
    st.title("🛠 CRUD Operations")
    crud_choice = st.selectbox("Choose Operation", ["Add Provider", "Delete Provider", "Add Food", "Delete Food"])

    if crud_choice == "Add Provider":
        with st.form("add_provider"):
            name = st.text_input("Provider Name")
            ptype = st.selectbox("Type", ["Restaurant", "Grocery Store", "Supermarket"])
            address = st.text_input("Address")
            city = st.text_input("City")
            contact = st.text_input("Contact")
            submitted = st.form_submit_button("Add Provider")
            if submitted:
                run_execute("INSERT INTO Providers(Name, Type, Address, City, Contact) VALUES (?, ?, ?, ?, ?)",
                            (name, ptype, address, city, contact))
                st.success("✅ Provider added successfully!")

    elif crud_choice == "Delete Provider":
        df = run_query("SELECT * FROM Providers")
        provider_id = st.selectbox("Select Provider ID to delete", df["Provider_ID"].tolist())
        if st.button("Delete Provider"):
            run_execute("DELETE FROM Providers WHERE Provider_ID = ?", (provider_id,))
            st.success("❌ Provider deleted successfully!")

    elif crud_choice == "Add Food":
        with st.form("add_food"):
            fname = st.text_input("Food Name")
            qty = st.number_input("Quantity", min_value=1)
            expiry = st.date_input("Expiry Date")
            pid = st.number_input("Provider ID", min_value=1)
            ftype = st.selectbox("Food Type", ["Vegetarian", "Non-Vegetarian", "Vegan"])
            meal = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Snacks"])
            submitted = st.form_submit_button("Add Food")
            if submitted:
                run_execute("INSERT INTO Food_Listings(Food_Name, Quantity, Expiry_Date, Provider_ID, Food_Type, Meal_Type) VALUES (?, ?, ?, ?, ?, ?)",
                            (fname, qty, expiry, pid, ftype, meal))
                st.success("✅ Food added successfully!")

    elif crud_choice == "Delete Food":
        df = run_query("SELECT * FROM Food_Listings")
        food_id = st.selectbox("Select Food ID to delete", df["Food_ID"].tolist())
        if st.button("Delete Food"):
            run_execute("DELETE FROM Food_Listings WHERE Food_ID = ?", (food_id,))
            st.success("❌ Food deleted successfully!")

# ==========================
# 4. SQL QUERIES & VISUALIZATION
# ==========================
elif choice == "SQL Queries & Visualization":
    st.title("📊 SQL Queries & Visualization")

    queries = {
        "1. All available food": 
        "SELECT Food_Name, Quantity, Expiry_Date FROM Food_Listings",

    "2. Expired food items": 
        "SELECT Food_Name, Quantity, Expiry_Date FROM Food_Listings WHERE date(Expiry_Date) < date('now')",

    "3. Providers per city": 
        "SELECT City, COUNT(*) as Count FROM Providers GROUP BY City",

    "4. Receivers per city": 
        "SELECT City, COUNT(*) as Count FROM Receivers GROUP BY City",

    "5. Top 5 providers by food items": 
        "SELECT p.Name, COUNT(*) as Food_Items FROM Providers p JOIN Food_Listings f ON p.Provider_ID=f.Provider_ID GROUP BY p.Name ORDER BY Food_Items DESC LIMIT 5",

    "6. Food listings by type": 
        "SELECT Food_Type, COUNT(*) as Count FROM Food_Listings GROUP BY Food_Type",

    "7. Food listings by meal type": 
        "SELECT Meal_Type, COUNT(*) as Count FROM Food_Listings GROUP BY Meal_Type",

    "8. Claims per status": 
        "SELECT Status, COUNT(*) as Count FROM Claims GROUP BY Status",

    "9. Most claimed food items": 
        "SELECT f.Food_Name, COUNT(c.Claim_ID) as Claims FROM Claims c JOIN Food_Listings f ON c.Food_ID=f.Food_ID GROUP BY f.Food_Name ORDER BY Claims DESC LIMIT 5",

    "10. Receivers with highest claims": 
        "SELECT r.Name, COUNT(c.Claim_ID) as Total_Claims FROM Claims c JOIN Receivers r ON c.Receiver_ID=r.Receiver_ID GROUP BY r.Name ORDER BY Total_Claims DESC LIMIT 5",

    "11. Providers contributing most vegetarian food": 
        "SELECT p.Name, COUNT(*) as Veg_Items FROM Providers p JOIN Food_Listings f ON p.Provider_ID=f.Provider_ID WHERE f.Food_Type='Vegetarian' GROUP BY p.Name ORDER BY Veg_Items DESC LIMIT 5",

    "12. Average quantity of food per provider": 
        "SELECT p.Name, AVG(f.Quantity) as Avg_Quantity FROM Providers p JOIN Food_Listings f ON p.Provider_ID=f.Provider_ID GROUP BY p.Name",

    "13. Providers with food expiring soon (2 days)": 
        "SELECT p.Name, f.Food_Name, f.Expiry_Date FROM Providers p JOIN Food_Listings f ON p.Provider_ID=f.Provider_ID WHERE date(f.Expiry_Date) <= date('now','+2 day')",

    "14. Total food quantity per city": 
        "SELECT p.City, SUM(f.Quantity) as Total_Quantity FROM Providers p JOIN Food_Listings f ON p.Provider_ID=f.Provider_ID GROUP BY p.City",

    "15. Completed claims with details": 
        "SELECT c.Claim_ID, f.Food_Name, r.Name as Receiver, p.Name as Provider, c.Timestamp FROM Claims c JOIN Food_Listings f ON c.Food_ID=f.Food_ID JOIN Providers p ON f.Provider_ID=p.Provider_ID JOIN Receivers r ON c.Receiver_ID=r.Receiver_ID WHERE c.Status='Completed'"
}

    qchoice = st.selectbox("Choose a query", list(queries.keys()))
    df = run_query(queries[qchoice])
    st.dataframe(df, use_container_width=True)

    # Visualization if numeric data
    if "Count" in df.columns or "Quantity" in df.columns:
        st.bar_chart(df.set_index(df.columns[0]))

# ==========================
# 5. LEARNER SQL QUERIES
# ==========================
elif choice == "Learner SQL Queries":
    st.title("👨‍🎓 Write Your Own SQL Query")
    query = st.text_area("Enter SQL Query")
    if st.button("Run Query"):
        try:
            df = run_query(query)
            st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error(f"⚠️ Error: {e}")

# ==========================
# 6. USER INTRODUCTION
# ==========================
elif choice == "User Introduction":
    st.title("🙋 About This Project")
    st.markdown("""
    **Project Developer:** Deepak Kumar  
    **Purpose:** Internship project to build a Local Food Wastage Management System.  
    **Tech Stack:** Streamlit, SQLite, Pandas, Python.  

    🚀 This project demonstrates:  
    - Building dashboards with Streamlit  
    - CRUD operations on SQLite  
    - Data visualization with SQL  
    """)
