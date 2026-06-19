import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Starzone12@",
    database="food_waste_management"
)

if conn.is_connected():
    print("Database connected successfully")

cursor = conn.cursor()
cursor.execute("SELECT * FROM providers")

result = cursor.fetchall()

for row in result:
    print(row)




    import streamlit as st
food_name = st.text_input("Food Name")
quantity = st.number_input("Quantity")

if st.button("Add Food"):
    query = "INSERT INTO food_listing_data (Food_Name, Quantity) VALUES (%s,%s)"
    cursor.execute(query, (food_name, quantity))
    conn.commit()
    st.success("Food Added")

import pandas as pd

cursor.execute("SELECT * FROM food_listing_data")

data = cursor.fetchall()

columns = [i[0] for i in cursor.description]

df = pd.DataFrame(data, columns=columns)

st.dataframe(df)