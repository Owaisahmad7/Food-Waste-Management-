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
    Large amounts of edible food are wasted every day by restaurants, supermarkets, and grocery stores
    while many individuals and organizations continue to face food shortages.
    """)

    st.subheader("Solution")

    st.write("""         
    This application connects food providers with receivers
    and helps monitor food donations using SQL analytics
    and interactive dashboards.
    """)

    st.markdown("---")

    st.subheader("Recommendation")
    
    st.write("""
    1-Prioritize High Contributing Providers 
    Dashboard shows supermarkets contribute more food donations""")
    st.write("""2-Improve Claim Completion Rate claim analysis shows
    Completed 33.9 Pending 32.5 Cancelled 33.6""")
    st.write("""3-Reduce Expired Food Waste""")
    st.write("""4-Focus on HighDemand Food Items. Providers should prioritize
    donating food categories that are claimed more frequently.""")
    st.write("""5-Expand in High Activity Cities""")
    st.write("""6-Track Provider Performance Create provider ranking and reward programs to encourage consistent food donations
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
        query = "SELECT * FROM food_listings LIMIT 1500"

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

    update_option = st.selectbox(
        "What do you want to update?",
        [
            "Quantity",
            "Expiry Date",
            "Meal Type"
        ]
    )

    # Update Quantity
    if update_option == "Quantity":

        new_quantity = st.number_input(
            "Enter New Quantity",
            step=1
        )

        if st.button("Update Quantity"):

            query = """
            UPDATE food_listings
            SET Quantity = %s
            WHERE Food_ID = %s
            """

            cursor.execute(
                query,
                (new_quantity, food_id)
            )

            conn.commit()

            st.success("Quantity Updated Successfully")

    # Update Expiry Date
    elif update_option == "Expiry Date":

        new_expiry = st.date_input(
            "Select New Expiry Date"
        )

        if st.button("Update Expiry Date"):

            query = """
            UPDATE food_listings
            SET Expiry_Date = %s
            WHERE Food_ID = %s
            """

            cursor.execute(
                query,
                (new_expiry, food_id)
            )

            conn.commit()

            st.success("Expiry Date Updated Successfully")

    # Update Meal Type
    elif update_option == "Meal Type":

        new_meal = st.selectbox(
            "Select New Meal Type",
            [
                "Breakfast",
                "Lunch",
                "Dinner",
                "Snacks"
            ]
        )

        if st.button("Update Meal Type"):

            query = """
            UPDATE food_listings
            SET Meal_Type = %s
            WHERE Food_ID = %s
            """

            cursor.execute(
                query,
                (new_meal, food_id)
            )

            conn.commit()

            st.success("Meal Type Updated Successfully")
elif menu == "Delete Food":
    st.subheader("Delete Food")

    # choose delete option
    delete_option = st.selectbox(
        "Choose Delete Option",
        [
            "Delete By Food ID",
            "Delete Expired Food"
        ]
    )

    # OPTION 1
    if delete_option == "Delete By Food ID":
        food_id = st.number_input("Enter Food ID", step=1)

        if st.button("Delete Food"):
            query = """
            DELETE FROM food_listings
            WHERE Food_ID = %s
            """

            cursor.execute(query, (food_id,))
            conn.commit()

            st.success("Food Deleted Successfully")

    # OPTION 2
    elif delete_option == "Delete Expired Food":
        cursor.execute("""
        SELECT Food_ID, Food_Name, Expiry_Date
        FROM food_listings
        WHERE Expiry_Date < CURDATE()
        """)

        data = cursor.fetchall()

        df = pd.DataFrame(
            data,
            columns=["Food ID", "Food Name", "Expiry Date"]
        )

        st.dataframe(df)

        # count expired food
        st.write("Total Expired Items:", len(df))

        # delete button
        if st.button("Delete Expired Food"):
            query = """
            DELETE FROM food_listings
            WHERE Expiry_Date < CURDATE()
            """

            cursor.execute(query)
            conn.commit()

            st.success("Expired Food Deleted Successfully")        
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

# Provider Type filter
    cursor.execute("SELECT DISTINCT Provider_Type FROM food_listings")
    provider_list = [row[0] for row in cursor.fetchall()]
    provider_list.insert(0, "All")

    selected_provider = st.selectbox(
    "Select Provider Type",
    provider_list
    )

# Meal Type filter
    cursor.execute("SELECT DISTINCT Meal_Type FROM food_listings")
    meal_list = [row[0] for row in cursor.fetchall()]
    meal_list.insert(0, "All")

    selected_meal = st.selectbox(
    "Select Meal Type",
    meal_list
    )
    # KPI - Total Food Listings after filter

    query = """
    SELECT COUNT(*)
    FROM food_listings
    WHERE (%s = 'All' OR Provider_Type = %s)
    AND (%s = 'All' OR Meal_Type = %s)
    """

    cursor.execute(query,(selected_provider,selected_provider,selected_meal,selected_meal))

    food_count = cursor.fetchone()[0]


    query = """
    SELECT SUM(Quantity)
    FROM food_listings
    WHERE (%s = 'All' OR Provider_Type = %s)
    AND (%s = 'All' OR Meal_Type = %s)
    """

    cursor.execute(query,(selected_provider,selected_provider,selected_meal,selected_meal))

    total_quantity = cursor.fetchone()[0]
    query = """
    SELECT COUNT(DISTINCT Provider_ID)
    FROM food_listings
    WHERE (%s = 'All' OR Provider_Type = %s)
    AND (%s = 'All' OR Meal_Type = %s)
    """

    cursor.execute(
    query,
    (
        selected_provider,
        selected_provider,
        selected_meal,
        selected_meal
    ))

    distinct_providers = cursor.fetchone()[0]
    query = """
    SELECT COUNT(DISTINCT Receiver_ID)
    FROM claim_data
    """

    cursor.execute(query)

    distinct_receivers = cursor.fetchone()[0]
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Food Listings", food_count)

    with col2:
        st.metric("Total Quantity", total_quantity)
    with col3:
        st.metric("Unique Provider", distinct_providers)
    with col4:
        st.metric("Unique Receivers", distinct_receivers)  

    query = """
    SELECT Food_Type, COUNT(*) AS Total
    FROM food_listings
    WHERE (%s='All' OR Provider_Type=%s)
    AND (%s='All' OR Meal_Type=%s)
    GROUP BY Food_Type
    """

    cursor.execute(
    query,
    (
        selected_provider,
        selected_provider,
        selected_meal,
        selected_meal
    )
    )

    data = cursor.fetchall()

    df = pd.DataFrame(
    data,
    columns=["Food Type", "Total"]
    )

    st.subheader("Food Type Distribution")

    st.bar_chart(
    df.set_index("Food Type")
    )
    query = """
    SELECT Meal_Type, COUNT(*) AS Total
    FROM food_listings
    WHERE (%s='All' OR Provider_Type=%s)
    AND (%s='All' OR Meal_Type=%s)
    GROUP BY Meal_Type
    """

    cursor.execute(
    query,
    (
        selected_provider,
        selected_provider,
        selected_meal,
        selected_meal
    )
    )

    data = cursor.fetchall()

    df = pd.DataFrame(
    data,
    columns=["Meal Type", "Total"]
    )

    fig, ax = plt.subplots()

    ax.pie(
    df["Total"],
    labels=df["Meal Type"],
    autopct="%1.1f%%"
    )

    st.subheader("Meal Type Distribution")

    st.pyplot(fig)
    query = """
    SELECT 
    Provider_ID,
    SUM(Quantity) AS Total
    FROM food_listings

    WHERE (%s='All' OR Provider_Type=%s)
    AND (%s='All' OR Meal_Type=%s)

    GROUP BY Provider_ID
    ORDER BY Total DESC
    LIMIT 10
    """

    cursor.execute(
    query,
    (
        selected_provider,
        selected_provider,
        selected_meal,
        selected_meal
    )
    )

    data = cursor.fetchall()

    df = pd.DataFrame(
    data,
    columns=["Provider ID", "Quantity"]
    )

    st.subheader("Top 10 Food Donors")

    st.bar_chart(
    df.set_index("Provider ID")
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

    fig, ax = plt.subplots()

    ax.pie(
    df["Total"],
    labels=df["Status"],
    autopct="%1.1f%%"
    )

    st.subheader("Claim Status Distribution")

    st.pyplot(fig)