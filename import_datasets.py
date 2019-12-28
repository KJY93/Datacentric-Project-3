import csv
import os
import pymysql

# database username
username = 'sql12317054'

# database host
hostname = 'sql12.freemysqlhosting.net'

# database = password
password = 'i4HZtC2C6y'

# database name
db_name = 'sql12317054'

# declare a list to keep the csv file
file_list = ['users.csv', 'manufacturer.csv', 'type.csv', 'ratings.csv', 'cereals.csv']

def main():
    try:
        
        # try to establish the connection to the database
        try: 
            connection = pymysql.connect(host=hostname, user=username, password=password, db=db_name)
            
            # declare cursor object
            cursor = connection.cursor()

        except pymysql.MySQLError as e:
            # print out the error
            print(f"Connection is not successful. Encountered error: {e}")

        for i in range(len(file_list)):
            try: 
                with open(file_list[i], "r") as csv_file:
                    
                    # declare a row count variable
                    row_count = 0;
                    
                    csv_reader = csv.reader(csv_file)

                    # skip the first row and save it to a variable
                    col_names = next(csv_reader)
                    
                    # join the list item into the sql query syntax
                    col_names_joined = ', '.join(col_names)           
                    
                    # define sql insert into syntax template
                    sql = f"INSERT INTO {file_list[i].split('.')[0].capitalize()}({col_names_joined}) VALUES"
                    
                    if file_list[i] == 'cereals.csv':
                    
                        # loop through the rest of the rows
                        for row in csv_reader:
                            
                            # initialize a row count variable to keep track of the number of rows in the csv file
                            row_count = row_count + 1

                            values = f"('{row[0]}', '{row[1]}', {row[2]}, {row[3]}, {row[4]}, {row[5]}, {row[6]}, {row[7]}, {row[8]}, {row[9]}, {row[10]}, {row[11]}, {row[12]}, {row[13]});"
                            
                            # get the full sql query stateement
                            sql_query = sql + values

                            # execute the query
                            cursor.execute(sql_query)

                            row_count = row_count
                            
                    elif ((file_list[i] == 'users.csv') or (file_list[i] == 'type.csv') or (file_list[i] == 'manufacturer.csv')):
                        
                        # loop through the rest of the rows
                        for row in csv_reader:
                            
                            # initialize a row count variable to keep track of the number of rows in the csv file
                            row_count = row_count + 1   
                                     
                            values = f"('{row[0]}');"
                            
                            # get the full sql query stateement
                            sql_query = sql + values
                        
                            # execute the query
                            cursor.execute(sql_query)

                            row_count = row_count
                        
                    elif (file_list[i] == 'ratings.csv'):
                        
                        # loop through the rest of the rows
                        for row in csv_reader:
                            
                            # initialize a row count variable to keep track of the number of rows in the csv file
                            row_count = row_count + 1   
                                     
                            values = f"('{row[0]}', '{row[1]}', '{row[2]}');"
                            
                            # get the full sql query stateement
                            sql_query = sql + values
                        
                            # execute the query
                            cursor.execute(sql_query)

                            row_count = row_count
                        
                            
                # commit all the rows to the respective tables in the database
                connection.commit()
                print(f"{row_count} rows are added to the {file_list[i].split('.')[0].capitalize()} table.")

            # print out the error if there is an error in opening the file
            except IOError as e:
                print("I/O error({0}): {1}".format(e.errno, e.strerror))

    except pymysql.MySQLError as e:
        # print out any mysql error raised
        print(e)

    finally:
        # closing the connection to the database
        # print out the connection closed message to the CLI
        connection.close()
        print("Database connection successfully closed.")

if __name__ == '__main__':
    main()

