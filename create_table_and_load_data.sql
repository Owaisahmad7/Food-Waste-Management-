SHOW VARIABLES LIKE 'local_infile';
SET GLOBAL local_infile = 1;
-- Load data from a local file
DROP TABLE IF EXISTS receivers_data;
CREATE TABLE providers(
 provider_id INT,
 Name VARCHAR(100),
 Type VARCHAR(50),
 Address VARCHAR(200),
 City VARCHAR(50),
 Contact VARCHAR(100)
);
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/providers_data.csv'
INTO TABLE providers
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
SHOW VARIABLES LIKE 'secure_file_priv';
/* Create a new table receivers and load data set from a local file */
CREATE TABLE receivers_data(
 Receiver_ID INT,
 Name VARCHAR(100),
 Type VARCHAR(50),
 City VARCHAR(50),
 Contact VARCHAR(100)
);
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/receivers_data.csv'
INTO TABLE receivers_data
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
/*Create a new table food listing data and load data set from a local file */   
create table food_listing_data(
 Food_ID INT,
 Food_Name VARCHAR(100),
 Quantity INT,
 Expiry_Date VARCHAR(50),
 Provider_ID INT,
 Provider_Type VARCHAR(100),
 Location VARCHAR(200),
 Food_Type VARCHAR(50),
 Meal_Type VARCHAR(50)
);
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/food_listings_data.csv'
INTO TABLE food_listing_data
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
/* Create a new table for claim data and load data set from a local file */
CREATE TABLE claim_data(
 Claim_ID INT,
 Food_ID INT,
 Receiver_ID INT,
 Status VARCHAR(100),
 Timestamp VARCHAR(50)
);
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/claims_data.csv'
INTO TABLE claim_data
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;