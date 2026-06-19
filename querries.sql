/* Joining tables*/
ALTER TABLE providers
ADD PRIMARY KEY (provider_id);
ALTER TABLE receivers_data
ADD PRIMARY KEY (Receiver_ID);
ALTER TABLE food_listing_data
ADD PRIMARY KEY (Food_ID),
ADD FOREIGN KEY (Provider_ID) REFERENCES providers(provider_id);
ALTER TABLE claim_data
ADD PRIMARY KEY (Claim_ID),
ADD FOREIGN KEY (Food_ID) REFERENCES food_listing_data(Food_ID),
ADD FOREIGN KEY (Receiver_ID) REFERENCES receivers_data(Receiver_ID);


/* The project will analyze food donations, claims, and provider trends using SQL queries. Below are some key questions:
Food Providers & Receivers
1.How many food providers and receivers are there in each city?
2.Which type of food provider (restaurant, grocery store, etc.) contributes the most food?
3.What is the contact information of food providers in a specific city?
4.Which receivers have claimed the most food?

Food Listings & Availability
5.What is the total quantity of food available from all providers?
6.Which city has the highest number of food listings?
7.What are the most commonly available food types?

Claims & Distribution
       8. How many food claims have been made for each food item?
       9. Which provider has had the highest number of successful food claims?
      10. What percentage of food claims are completed vs. pending vs. canceled?

Analysis & Insights
       11. What is the average quantity of food claimed per receiver?
       12. Which meal type (breakfast, lunch, dinner, snacks) is claimed the most?
What is the total quantity of food donated by each provider?

*/
SELECT 
    City,
    COUNT(*) AS total_providers
FROM providers
GROUP BY City;
SELECT 
    City,
    COUNT(*) AS total_receivers
FROM receivers_data
GROUP BY City;
-- In a single querry

SELECT 
    p.City,
    COUNT(DISTINCT p.Provider_ID) AS total_providers,
    COUNT(DISTINCT r.Receiver_ID) AS total_receivers
FROM providers p
LEFT JOIN receivers_data r
    ON p.City = r.City
GROUP BY p.City;

/*928 Cities have only one provider 
33 Cities has two providers
while only two cities "New Carol" and "South Christopherborough have three providers"*/
SELECT 
    City,
    COUNT(DISTINCT Receiver_ID) AS Total_Receivers
FROM receivers_data
GROUP BY City
HAVING COUNT(DISTINCT Receiver_ID) = 3;
/*933 Cities have only one receiver ,
32 Cities has two receivers while only city "New Christopher"has three receivers
*/

/*Which type of food provider (restaurant, grocery store, etc.) contributes the most food?*/
SELECT 
    Type,
    COUNT(*) AS Total_Donations
FROM providers
GROUP BY Type
ORDER BY Total_Donations DESC;
/*most provider food type is Supermarket with 262 providers followed by grocery store with 256 providers and restaurant with 246 providers*/
/*What is the contact information of food providers in a specific city?*/
SELECT City, Contact
FROM providers
ORDER BY City;
/*Which receivers have claimed the most food?*/
SELECT Type, COUNT(*) AS Total_received
FROM receivers_data
GROUP BY Type
ORDER BY Total_received DESC;
/*NGO has received the most food 274 times*/
/*
What is the total quantity of food available from all providers?
*/
SELECT SUM(Quantity) AS Total_Food_Quantity
FROM food_listing_data;
/*
Total quantity of food available from all providers is 25794 units
*/
/*Which city has the highest number of food listings?*/
SELECT Location, COUNT(*) AS Total_Listings
FROM food_listing_data 
GROUP BY Location
ORDER BY Total_Listings DESC
LIMIT 1;
/*The city with the highest number of food listings is New Christopher with 6 listings*/
/*What are the most commonly available food types?*/
SELECT Food_Type, COUNT(*) AS Availability
FROM food_listing_data
GROUP BY Food_Type
ORDER BY Availability DESC;
/*The most commonly available food type is Vegetarian with 336 listings followed by Vegan with 334 listings and NON-VEGETARIAN with 330 listings*/
/*How many food claims have been made for each food item?*/
SELECT 
    f.Food_Name,
    COUNT(c.Claim_ID) AS total_claims
FROM food_listing_data f
JOIN claim_data c
    ON f.Food_ID = c.Food_Id
GROUP BY f.Food_Name
ORDER BY total_claims DESC;
/*Which provider has had the highest number of successful food claims?*/
SELECT c.Status, COUNT(WHERE Status = "Complete")
FROM claim_data
JOIN food_listing_data f 
   ON f.Food_ID = c.Food_ID
GROUP BY f.Provider_Type;

SELECT 
    p.Name,
    COUNT(c.Claim_ID) AS successful_claims
FROM providers p
JOIN food_listing_data f
    ON p.provider_id = f.Provider_ID
JOIN claim_data c
    ON f.Food_ID = c.Food_ID
WHERE c.Status = 'Completed'
GROUP BY p.Name
ORDER BY successful_claims DESC;
/*Barry Group is the highest successful provider*/

SELECT 
    f.Provider_ID,
    COUNT(c.Claim_ID) AS successful_claims
FROM food_listing_data f
JOIN claim_data c
    ON f.Food_ID = c.Food_ID
WHERE c.Status = 'Completed'
GROUP BY f.Provider_ID
ORDER BY successful_claims DESC;
/* 10. What percentage of food claims are completed vs. pending vs. canceled? */
SELECT 
    Status,
    COUNT(*) AS total_claims,
    ROUND(
        COUNT(*) * 100.0 / (SELECT COUNT(*) FROM claim_data),
        2
    ) AS percentage
FROM claim_data
GROUP BY Status;
/*Completed=33.90, pending= 32.50 and Cancelled =33.60*/
/*11. What is the average quantity of food claimed per receiver? */
SELECT c.Receiver_ID, AVG(f.Quantity) AS Average_food
FROM claim_data c
JOIN food_listing_data f
ON c.Food_ID = f.Food_ID
GROUP BY Receiver_ID;
/*12. Which meal type (breakfast, lunch, dinner, snacks) is claimed the most?
What is the total quantity of food donated by each provider?
*/
SELECT 
    f.Meal_Type,
    COUNT(c.Claim_ID) AS total_claims
FROM claim_data c
JOIN food_listing_data f
    ON c.Food_ID = f.Food_ID
GROUP BY f.Meal_Type
ORDER BY total_claims DESC;

SELECT 
    p.Name,
    SUM(f.Quantity) AS total_food_donated
FROM providers p
JOIN food_listing_data f
    ON p.Provider_ID = f.Provider_ID
GROUP BY p.Name
ORDER BY total_food_donated DESC;
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
