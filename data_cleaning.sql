/* TABLE FIRST LOOK*/
SELECT * FROM providers Limit 10;
/* Check Structure of the table */
DESCRIBE providers;

/*Find out the nulls/blanks in the table*/
SELECT *
FROM providers
WHERE Name IS NULL
   OR Name = '';
   -- Checking it in more detail sometimes the nulls are represented as 'NA', 'N/A', '-', 'null' etc. So we will check for those as well
SELECT *
FROM providers
WHERE Name IN ('NA', 'N/A', '-', 'null',' ');
-- There are no null values in the Name
SELECT *
FROM providers
WHERE provider_id IS NULL
   OR provider_id = '';
SELECT *
FROM providers
WHERE Type IS NULL
   OR Type = '';
SELECT *
FROM providers
WHERE Address IS NULL
   OR Address = '';  
   SELECT *
FROM providers
WHERE City IS NULL
   OR City = '';
SELECT *
FROM providers
WHERE Contact IS NULL
   OR Contact = '';

UPDATE providers
SET Name = "Nguyen Inc"
WHERE provider_id = 9;
SELECT
    COUNT(*) AS Total_Rows,
    SUM(CASE WHEN provider_id IS NULL THEN 1 ELSE 0 END) AS Null_provider_id,
    SUM(CASE WHEN Name IS NULL OR Name = '' THEN 1 ELSE 0 END) AS Null_or_Blank_Name,
    SUM(CASE WHEN Type IS NULL OR Type = '' THEN 1 ELSE 0 END) AS Null_or_Blank_Type,
    SUM(CASE WHEN Address IS NULL OR Address = '' THEN 1 ELSE 0 END) AS Null_or_Blank_Address,
    SUM(CASE WHEN City IS NULL OR City = '' THEN 1 ELSE 0 END) AS Null_or_Blank_City,
    SUM(CASE WHEN Contact IS NULL OR Contact = '' THEN 1 ELSE 0 END) AS Null_or_Blank_Contact
FROM providers;
/* Checking forDuplicate values for table providers*/
SELECT provider_id, COUNT(*)
FROM providers
GROUP BY provider_id
HAVING COUNT(*) > 1;

/*Clean the Name,Type,Address,City and Contact Column*/
UPDATE providers
SET Name = TRIM(Name),
    Type = TRIM(Type),
    Address = TRIM(Address),
    City = TRIM(City),
    Contact= TRIM(Contact);
-- Clean the Contact column    

SELECT Contact
FROM providers
WHERE Contact LIKE '%x%'
   OR Contact LIKE '%-%'
   OR Contact LIKE '%.%'
   OR Contact LIKE '%(%';
   /*Cleaning the Contact column */
   -- We will first remove the extension part of the contact number which is after 'x' and then we will remove any special characters like '-', '.', '(', ')'
UPDATE providers
SET Contact = SUBSTRING_INDEX(Contact, 'x', 1);
UPDATE providers
SET Contact = REPLACE(Contact, '-','');
UPDATE providers
SET Contact = REPLACE(Contact, '.','');
UPDATE providers
SET Contact = REPLACE(Contact, '(', '');
UPDATE providers
SET Contact = REPLACE(Contact, ')', '');
-- After cleaning the contact column we will check for any remaining special characters
SELECT Contact
FROM providers
WHERE Contact LIKE '%x%'
   OR Contact LIKE '%-%'
   OR Contact LIKE '%.%'
   OR Contact LIKE '%(%'
   OR Contact LIKE '%)%';
SELECT Contact
FROM providers
LIMIT 20;
/* Cleaning the table Receivers */
DESCRIBE receivers_data;
select Receiver_ID
FROM receivers_data
WHERE Receiver_ID IS NULL
   or Receiver_ID ='';
SELECT COUNT(*) AS Total_Rows,
    SUM(CASE WHEN Receiver_ID IS NULL OR Receiver_ID = '' THEN 1 ELSE 0 END) AS Null_Receiver_ID,
    SUM(CASE WHEN Name IS NULL OR Name = '' THEN 1 ELSE 0 END) AS Null_or_Blank_Name,
    SUM(CASE WHEN Type IS NULL OR Type = '' THEN 1 ELSE 0 END) AS Null_or_Blank_Type,
    SUM(CASE WHEN City IS NULL OR City = '' THEN 1 ELSE 0 END) AS Null_or_Blank_City,
    SUM(CASE WHEN Contact IS NULL OR Contact = '' THEN 1 ELSE 0 END) AS Null_or_Blank_Contact
FROM receivers_data;
SELECT *
FROM receivers_data
WHERE City IN ('NA', 'N/A', '-', 'null',' ');
/* Checking for duplicate values in the Receivers table */
SELECT Receiver_ID, COUNT(*)
FROM receivers_data
GROUP BY Receiver_ID
HAVING COUNT(*) > 1;
/*Cleaning the Name , Type, City and Contact Column*/
UPDATE receivers_data
SET Name = TRIM(Name),
    Type = TRIM(Type),
    City = TRIM(City);
/* Cleaning the Contact column */
UPDATE receivers_data
SET Contact = TRIM(Contact);  
SELECT Contact
FROM receivers_data
WHERE Contact LIKE '%x%'
   OR Contact LIKE '%-%'
   OR Contact LIKE '%.%'
   OR Contact LIKE '%(%';
UPDATE receivers_data
SET Contact = SUBSTRING_INDEX(Contact, 'x', 1),
    Contact = REPLACE(Contact, '-',''),
    Contact = REPLACE(Contact, '.',''),
    Contact = REPLACE(Contact, '(', ''),
    Contact = REPLACE(Contact, ')', '');
SELECT Contact from receivers_data;
/* CLEANING TABBLE Food_listing*/
/*Describe the structure of the Food_listing table */
DESCRIBE food_listing_data;
/*Check for null or blank values */
   SELECT COunt(*) AS Total_Rows,
      SUM(CASE WHEN Food_ID IS NULL OR Food_ID = '' THEN 1 ELSE 0 END) AS Null_Food_ID,
      SUM(CASE WHEN Food_Name IS NULL OR Food_Name ='' THEN 1 ELSE 0 END ) AS Null_Food_Name,
      SUM(CASE WHEN Quantity IS NULL OR Quantity = '' THEN 1 ELSE 0 END) AS Null_QUANTITY,
      SUM(CASE WHEN Expiry_Date IS NULL OR Expiry_Date = '' THEN 1 ELSE 0 END) AS Null_EXPIRY_DATE,
      SUM(CASE WHEN Provider_ID IS NULL OR Provider_ID = '' THEN 1 ELSE 0 END) AS Null_PROVIDER_ID,
      SUM (CASE WHEN Provider_Type IS NULL OR Provider_Type = '' THEN 1 ELSE 0 END) AS Null_Provider_Type,
      SUM(CASE WHEN Location IS NULL OR Location = '' THEN 1 ELSE 0 END) AS Null_Location,
      SUM(CASE WHEN Food_Type IS NULL OR Food_Type = '' THEN 1 ELSE 0 END) AS Null_Food_Type,
      SUM(CASE WHEN Meal_Type IS NULL OR Meal_Type = '' THEN 1 ELSE 0 END) AS Null_Meal_Type
FROM food_listing_data;
SELECT * FROM food_listing_data
WHERE Food_ID IN ('NA', 'N/A', '-', 'null',' ');
/*Checking for duplicate values in the Food_listing table */
SELECT Food_ID, COUNT(*)
FROM food_listing_data
GROUP BY Food_ID
HAVING COUNT(*) > 1;

/*Cleaning the Food_Name, Provider_Type, Location, Food_Type and Meal_Type column*/
UPDATE food_listing_data
SET Food_Name = TRIM(Food_Name),
      Provider_Type = TRIM(Provider_Type),
      Location = TRIM(Location),
      Food_Type = TRIM(Food_Type),
      Meal_Type = TRIM(Meal_Type),
      Expiry_Date = TRIM(Expiry_Date);
/*AS I have imported Expiry_Date as VARCHAR Data type 
so ..Test conversion first */      
SELECT Expiry_Date,
       STR_TO_DATE(Expiry_Date, '%m/%d/%Y') AS converted_date
FROM food_listing_data; 
/* Conversion looks fine So now we will upadte the values  */
UPDATE food_listing_data
SET Expiry_Date = STR_TO_DATE(Expiry_Date, '%m/%d/%Y');
/*Still the column data type is VARCHAR Now i will change the data type*/
ALTER TABLE food_listing_data
MODIFY COLUMN Expiry_Date DATE;
Describe food_listing_data;
/*Cleaning the Claims_data table*/
/*Checking the null values */
SELECT COUNT(*) AS Total_Rows,
      SUM(CASE WHEN Claim_ID IS NULL OR Claim_ID = '' THEN 1 ELSE 0 END) AS Null_Claim_ID,
      SUM(CASE WHEN Food_ID IS NULL OR Food_ID = '' THEN 1 ELSE 0 END ) AS Null_Food_ID,
      SUM(CASE WHEN Receiver_ID IS NULL OR Receiver_ID = '' THEN 1 ELSE 0 END) AS Null_Receiver_ID,
      SUM(CASE WHEN Status IS NULL OR Status = '' THEN 1 ELSE 0 END ) AS Null_Status,
      SUM(CASE WHEN Timestamp IS NULL OR Timestamp = '' THEN 1 ELSE 0 END ) AS Null_Timestamp
FROM claim_data;  
SELECT * FROM claim_data
WHERE Claim_ID IN ('NA', 'N/A', '-', 'null',' ');   
 /*Checking and removing duplicates*/
SELECT Claim_ID,COUNT(*)
From claim_data
Group BY Claim_ID
HAVING COUNT(*) >1; 
SELECT * FROM claim_data
WHERE(Claim_ID, Food_ID, Receiver_ID, Status) IN (SELECT Claim_ID, Food_ID, Receiver_ID, Status
FROM claim_data
GROUP BY Claim_ID, Food_ID, Receiver_ID, Status
HAVING COUNT(*) > 1);   
/*Cleaning the Varchar datatype columns*/
UPDATE claim_data
SET Status = TRIM(Status),
     Timestamp = TRIM(Timestamp);
/*Changing data type of Timestamp to DATETIME*/
-- Preview the Conversion
SELECT Timestamp,
       STR_TO_DATE(Timestamp, '%m/%d/%Y %H:%i') AS Converted
FROM claim_data;
-- Update the values
UPDATE claim_data
SET Timestamp = STR_TO_DATE(Timestamp, '%m/%d/%Y %H:%i');
-- Change the data type
ALTER TABLE claim_data
MODIFY COLUMN Timestamp DATETIME;
/*Describe the claim_data table after cleaning*/
DESCRIBE claim_data;
/*Export cleaned data to CSV files*/

SELECT *
INTO OUTFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/providers_cleaned.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
FROM providers;
SELECT *
INTO OUTFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\receivers_cleaned.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
FROM receivers_data;
SELECT *
INTO OUTFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\food_listing_cleaned.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
FROM food_listing_data;
SELECT *
INTO OUTFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\claims_cleaned.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
FROM claim_data;

