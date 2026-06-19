import streamlit as st
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Starzone12@",
    database="food_waste_management"
)

if conn.is_connected():
    print("Database connected successfully")

cursor = conn.cursor()

# Title
st.title("Food Wastage Management System")


# Sidebar
menu = st.sidebar.selectbox(
    "Choose Section",
    [
        "Home",
        "Dashboard",
        "SQL Insights",
        "Add Food",
        "View Food",
        "Update Food",
        "Delete Food"
        
        
    ]
)
# HOME PAGE
if menu == "Home":
    st.image("food_waste.jpg", width=700)   # optional image

    st.markdown("---")

    st.subheader("Problem Statement")

    st.write("""
    Large quantities of food are wasted every day by restaurants,
    supermarkets, and grocery stores while many people face food insecurity.
    """)

    st.subheader("Solution")

    st.write("""
    This application connects food providers with receivers
    and helps monitor food donations using SQL analytics
    and interactive dashboards.
    """)

    st.markdown("---")

    st.subheader("Technology Used")

    st.write("""
    • Python  
    • MySQL  
    • Streamlit  
    • Pandas  
    • Matplotlib  
    • SQL Queries for Insights  
    """)

    st.markdown("---")
#Add food
elif menu == "Add Food":

    st.subheader("Add Food")

    # Inputs
    food_id = st.number_input("Food ID", step=1)

    food_name = st.text_input("Food Name")

    quantity = st.number_input("Quantity", step=1)

    expiry_date = st.date_input("Expiry Date")

    provider_id = st.number_input("Provider ID", step=1)

    provider_type = st.text_input("Provider Type")

    location = st.text_input("Location")

    food_type = st.selectbox(
        "Food Type",
        ["Non-Vegetarian", "Vegetarian", "Vegan"]
    )

    meal_type = st.selectbox(
        "Meal Type",
        ["Breakfast", "Dinner", "Lunch", "Snacks"]
    )

    # Button
    if st.button("Add Food"):

        query = """
        INSERT INTO food_listings
        (Food_ID, Food_Name, Quantity, Expiry_Date,
         Provider_ID, Provider_Type, Location,
         Food_Type, Meal_Type)

        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """

        values = (
            food_id,
            food_name,
            quantity,
            expiry_date,
            provider_id,
            provider_type,
            location,
            food_type,
            meal_type
        )

        cursor.execute(query, values)

        conn.commit()

        st.success("Food Added Successfully")
elif menu == "View Food":

    st.subheader("View Food Listings")

    try:
        query = "SELECT * FROM food_listings LIMIT 100"

        cursor.execute(query)

        data = cursor.fetchall()

        columns = [i[0] for i in cursor.description]

        df = pd.DataFrame(data, columns=columns)

        st.write("Total Records:", len(df))

        st.dataframe(df, use_container_width=True)

    except Exception as e:
        st.error(e) 
elif menu == "Update Food":

    st.subheader("Update Food")

    food_id = st.number_input("Enter Food ID", step=1)

    new_quantity = st.number_input("New Quantity", step=1)

    if st.button("Update"):

        query = """
        UPDATE food_listings
        SET Quantity = %s
        WHERE Food_ID = %s
        """

        cursor.execute(query, (new_quantity, food_id))

        conn.commit()

        st.success("Updated Successfully")
elif menu == "Delete Food":

    st.subheader("Delete Food")

    food_id = st.number_input("Enter Food ID", step=1)

    if st.button("Delete"):

        query = """
        DELETE FROM food_listings
        WHERE Food_ID = %s
        """

        cursor.execute(query, (food_id,))

        conn.commit()

        st.success("Deleted Successfully")
elif menu == "SQL Insights":

    st.subheader("SQL Business Insights")

    insight = st.selectbox(
        "Choose Insight",
        [
            "Providers and Receivers by City",
            "Provider Type Contribution",
            "Total Food Quantity",
            "City With Highest Listings",
            "Food Type Availability",
            "Most Claimed Food Items",
            "Claim Status Percentage",
            "Average Food Claimed Per Receiver",
            "Total Quantity Donated By Each Provider",
            "Most Claimed Meal Type"
        ]
    )
    if insight == "Providers and Receivers by City":
        query = """
        SELECT 
        p.City,
        COUNT(DISTINCT p.Provider_ID) AS total_providers,
        COUNT(DISTINCT r.Receiver_ID) AS total_receivers
        FROM providers p
        LEFT JOIN receivers_data r
        ON p.City = r.City
        GROUP BY p.City
        """
        cursor.execute(query)

        data = cursor.fetchall()
        df = pd.DataFrame(data,columns=["City", "Providers", "Receivers"])
        st.dataframe(df)
        st.success("Shows food ecosystem distribution by city")                               

    if insight == "Provider Type Contribution":
        query = """SELECT Type, COUNT(*) AS Total_Donations
        FROM providers
        GROUP BY Type
        ORDER BY Total_Donations DESC
        """

        cursor.execute(query)

        data = cursor.fetchall()

        df = pd.DataFrame(
        data,
        columns=["Provider Type", "Total Donations"]
        )

        st.dataframe(df)

        st.info("Supermarkets contribute the highest food donations")  
    if insight == "Total Food Quantity":
        query = """
        SELECT SUM(Quantity) AS Total_Food_Quantity
        FROM food_listings
        """

        cursor.execute(query)

        result = cursor.fetchone()

        st.metric(
        "Total Food Available",
        result[0]
        )
    if insight == "Claim Status Percentage":
        query = """
        SELECT 
        Status,
        COUNT(*) AS total_claims,
        ROUND(
            COUNT(*) * 100.0 /
            (SELECT COUNT(*) FROM claim_data),
            2
        ) AS percentage
        FROM claim_data
        GROUP BY Status
        """

        cursor.execute(query)

        data = cursor.fetchall()

        df = pd.DataFrame(
        data,
        columns=["Status", "Total Claims", "Percentage"]
        )

        st.dataframe(df)
    if insight == "Most Claimed Meal Type":
        query = """
        SELECT 
        f.Meal_Type,
        COUNT(c.Claim_ID) AS total_claims
        FROM claim_data c
        JOIN food_listings f
        ON c.Food_ID = f.Food_ID
        GROUP BY f.Meal_Type
        ORDER BY total_claims DESC
        """

        cursor.execute(query)

        data = cursor.fetchall()
 
        df = pd.DataFrame(
        data,
        columns=["Meal Type", "Claims"]
        )
        st.dataframe(df)
    if insight == "City With Highest Listings":
        query = """
        SELECT Location, COUNT(*) AS Total_Listings
        FROM food_listings
        GROUP BY Location
        ORDER BY Total_Listings DESC
        LIMIT 1
        """

        cursor.execute(query)

        result = cursor.fetchone()

        city = result[0]
        listings = result[1]

        st.metric("Top City",city)

        st.metric("Total Listings",listings)

        st.success(
        f"{city} has the highest number of food listings."
        )       
    if insight == "Most Claimed Food Items":
        query = """
        SELECT 
        f.Food_Name,
        COUNT(c.Claim_ID) AS total_claims
        FROM food_listings f
        JOIN claim_data c
        ON f.Food_ID = c.Food_ID
        GROUP BY f.Food_Name
        ORDER BY total_claims DESC
        """

        cursor.execute(query)

        data = cursor.fetchall()

        df = pd.DataFrame(
        data,
        columns=["Food Item", "Total Claims"]
        )

        st.subheader("Most Claimed Food Items")

        st.dataframe(df, use_container_width=True)
    if insight == "Average Food Claimed Per Receiver":
        query = """
        SELECT 
        c.Receiver_ID,
        AVG(f.Quantity) AS Average_Food
        FROM claim_data c
        JOIN food_listings f
        ON c.Food_ID = f.Food_ID
        GROUP BY c.Receiver_ID
        ORDER BY Average_Food DESC
        """

        cursor.execute(query)

        data = cursor.fetchall()

        df = pd.DataFrame(
        data,
        columns=["Receiver ID", "Average Food Quantity"]
        )

        st.subheader("Average Food Claimed Per Receiver")

        st.dataframe(df, use_container_width=True)
    if insight == "Food Type Availability":
        query = """
        SELECT 
        Food_Type,
        COUNT(*) AS Availability
        FROM food_listings
        GROUP BY Food_Type
        ORDER BY Availability DESC
        """

        cursor.execute(query)

        data = cursor.fetchall()

        df = pd.DataFrame(
        data,
        columns=["Food Type", "Available Listings"]
        )

        st.subheader("Food Type Availability")

        st.dataframe(df, use_container_width=True)
    if insight == "Total Quantity Donated By Each Provider":
        query = """
        SELECT 
        p.Name,
        SUM(f.Quantity) AS total_food_donated
        FROM providers p
        JOIN food_listings f
        ON p.Provider_ID = f.Provider_ID
        GROUP BY p.Name
        ORDER BY total_food_donated DESC
        """

        cursor.execute(query)

        data = cursor.fetchall()

        df = pd.DataFrame(
        data,
        columns=["Provider Name", "Total Food Donated"]
        )

        st.subheader("Total Quantity Donated By Each Provider")

        st.dataframe(df, use_container_width=True)
elif menu == "Dashboard":
    st.subheader("Analytics Dashboard")
        #KPI 1
    cursor.execute("SELECT COUNT(*) FROM providers")
    providers = cursor.fetchone()[0]

    # KPI 2
    cursor.execute("SELECT COUNT(*) FROM receivers_data")
    receivers = cursor.fetchone()[0]

    # KPI 3
    cursor.execute("SELECT COUNT(*) FROM food_listings")
    food_listings = cursor.fetchone()[0]

    # KPI 4
    cursor.execute("SELECT COUNT(*) FROM claim_data")
    claims = cursor.fetchone()[0]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Providers", providers)

    with col2:
        st.metric("Receivers", receivers)

    with col3:
        st.metric("Food Listings", food_listings)

    with col4:
        st.metric("Claims", claims)
        query = """
    SELECT Food_Type, COUNT(*) AS Count
    FROM food_listings
    GROUP BY Food_Type
    """

    cursor.execute(query)

    data = cursor.fetchall()

    df = pd.DataFrame(
        data,
        columns=["Food Type", "Count"]
    )

    st.subheader("Food Type Distribution")

    st.bar_chart(
        df.set_index("Food Type")
    )
    query = """
    SELECT Status, COUNT(*) AS Total
    FROM claim_data
    GROUP BY Status
    """

    cursor.execute(query)

    data = cursor.fetchall()

    df = pd.DataFrame(
        data,
        columns=["Status", "Total"]
    )

    st.subheader("Claim Status Distribution")

    st.bar_chart(
        df.set_index("Status")
    )   
    query = """
    SELECT Type, COUNT(*) AS Total
    FROM providers
    GROUP BY Type
    """

    cursor.execute(query)

    data = cursor.fetchall()

    df = pd.DataFrame(
        data,
        columns=["Provider Type", "Total"]
    )

    st.subheader("Provider Type Contribution")
    fig, ax = plt.subplots()

    colors = ["red", "blue", "green", "orange"]

    ax.bar(
    df["Provider Type"],
    df["Total"],
    color=colors
    )

    ax.set_title("Provider Type Contribution")
    ax.set_xlabel("Provider Type")
    ax.set_ylabel("Total Providers")

    st.pyplot(fig)
   
    query = """
    SELECT 
        p.Name,
        SUM(f.Quantity) AS total_food
    FROM providers p
    JOIN food_listings f
        ON p.Provider_ID = f.Provider_ID
    GROUP BY p.Name
    ORDER BY total_food DESC
    LIMIT 10
    """

    cursor.execute(query)

    data = cursor.fetchall()

    df = pd.DataFrame(
        data,
        columns=["Provider", "Quantity"]
    )

    st.subheader("Top 10 Food Donors")

    st.bar_chart(
        df.set_index("Provider")
    ) 
