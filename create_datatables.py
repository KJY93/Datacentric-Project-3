import os
import pymysql

# database username
username = os.environ.get("MYSQL_USER")

# database host
hostname = os.environ.get("MYSQL_HOST")

# database = password
password = os.environ.get("MYSQL_PASSWORD")

# database name
db_name = os.environ.get("MYSQL_DB")

# declare a list containing all the create table sql syntax
sql = [
    
'''CREATE TABLE Users (user_id INTEGER AUTO_INCREMENT PRIMARY KEY, name varchar(255) NOT NULL UNIQUE, password varchar(255) NOT NULL);''',
    
'''CREATE TABLE Manufacturer (manufacturer_id INTEGER AUTO_INCREMENT PRIMARY KEY, manufacturer_description varchar(100) NOT NULL UNIQUE);''',

'''CREATE TABLE Type (type_id INTEGER AUTO_INCREMENT PRIMARY KEY, cereals_type varchar(10) NOT NULL);''', 

# need to commit 4/1/2020 (no need coz change back to int already)
'''CREATE TABLE Cereals (cereal_id INTEGER AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100) NOT NULL UNIQUE, manufacturer_id INTEGER, FOREIGN KEY (manufacturer_id) REFERENCES Manufacturer (manufacturer_id),
type_id INTEGER, FOREIGN KEY (type_id) REFERENCES Type (type_id), calories INTEGER, protein INTEGER, fat INTEGER, sodium INTEGER, fiber INTEGER, carbohydrates INTEGER,
sugars INTEGER, potassium INTEGER, vitamins INTEGER);''',

# need to commit 4/1/2020
'''CREATE TABLE Ratings (rating_id INTEGER AUTO_INCREMENT PRIMARY KEY, ratings FLOAT, comment VARCHAR(255), user_id INTEGER, FOREIGN KEY (user_id) REFERENCES Users (user_id),
cereal_id INTEGER, FOREIGN KEY (cereal_id) REFERENCES Cereals (cereal_id));''',

'''CREATE TABLE Contribute (contribute_id INTEGER AUTO_INCREMENT PRIMARY KEY, user_id INTEGER, FOREIGN KEY (user_id) REFERENCES Users (user_id),
manufacturer_id INTEGER, FOREIGN KEY (manufacturer_id) REFERENCES Manufacturer (manufacturer_id), cereal_id INTEGER, FOREIGN KEY (cereal_id) REFERENCES Cereals (cereal_id));'''

]

try:
    
    # try to establish the connection to the database
    try: 
        connection = pymysql.connect(host=hostname, user=username, password=password, db=db_name)
        
    except pymysql.MySQLError as e:
        # print out the error
        print(f"Connection is not successful. Encountered error: {e}")
        
    with connection.cursor() as cursor:
        for tables in sql:
            cursor.execute(tables)

finally:
    # close the connection to the database
    connection.close(); 
