import os
import re 

from flask import Flask, session, request, redirect, render_template, url_for, flash, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session
from flask_mysqldb import MySQL


app = Flask(__name__)

# Setting the secret key
app.secret_key = 'Kde2J6H48klxGmEmbVZq0A' 

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Setting up the configurations needed to access the MySQL database in phpMyAdmin

app.config['MYSQL_USER'] = os.environ.get("MYSQL_USER")
app.config['MYSQL_PASSWORD'] = os.environ.get("MYSQL_PASSWORD")
app.config['MYSQL_HOST'] = 'remotemysql.com'
app.config['MYSQL_DB'] = '08SUJq26f2'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# Index Page
@app.route('/', methods=["GET", "POST"])
def index():
    if "user" in session:
        # Query for all the cereal items in the Cereals table
        cursor = mysql.connection.cursor()

        cursor.execute(('''SELECT Cereals.name, manufacturer_description, Type.cereals_type, Cereals.calories,
                Cereals.protein, Cereals.fat, Cereals.sodium, Cereals.fiber, Cereals.carbohydrates, Cereals.sugars,
                Cereals.potassium, Cereals.vitamins FROM Cereals INNER JOIN Manufacturer ON Cereals.manufacturer_id =
                Manufacturer.manufacturer_id INNER JOIN Type ON Cereals.type_id = Type.type_id ORDER BY Cereals.calories DESC'''))

        cereals_menu = cursor.fetchall()

        # declare an empty variable to store all the cereals item
        cereal_menu_item = []
        
        for i in range(len(cereals_menu)):
            cereal_menu_item.append(cereals_menu[i]['name'])
            
        # record the number of rows in the cereals table
        cereal_record_count = len(cereals_menu)
        
        # loop through the first row of record returned from the database to get the column headers
        col_headers = cereals_menu[0].keys()
        
        # Count all rows for a particular manufacturer category
        cursor.execute('''SELECT Manufacturer.manufacturer_description, COUNT(*) as count FROM Cereals INNER JOIN Manufacturer ON
                    Cereals.manufacturer_id = Manufacturer.manufacturer_id GROUP BY Cereals.manufacturer_id''')
        
        cereal_item_manufacturer_count = cursor.fetchall()
        
        # Get all the manufacturer
        cursor.execute('''SELECT manufacturer_description FROM Manufacturer''')
        
        manufacturer_category_description = cursor.fetchall()
        
        # declare an empty variable to store the manufacturers
        manufacturer_category_description_array = []
        
        for j in manufacturer_category_description:
            manufacturer_category_description_array.append(j['manufacturer_description'])
            
        return render_template('index.html', cereal_menu_item=cereal_menu_item, manufacturer_category_description_array=manufacturer_category_description_array, col_headers=col_headers, cereals_menu=cereals_menu, cereal_item_manufacturer_count=cereal_item_manufacturer_count, cereal_record_count=cereal_record_count)
    
    else:
        return render_template("login.html")
        
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        # Ensure username is submitted
        if not request.form.get("username"):
            return render_template("error.html", message="Error message: Username field is empty. Please complete all the fields before logging in.")

        # Ensure password is submitted
        if not request.form.get("password"):
            return render_template("error.html", message="Error message: Password field is empty. Please complete all the fields before logging in.")

        # Query database for username
        name = request.form.get("username")
        
        cursor = mysql.connection.cursor()
    
        cursor.execute('''SELECT user_id, name, password FROM Users WHERE name=''' + "\'" + name + "\'")
        
        user_login = cursor.fetchone()
                
        if user_login == None:
            flash("Username does not exist. Please register.")
            return redirect(url_for('register'))
              
        elif len(user_login) !=0:
            password = request.form.get("password")
            if check_password_hash(user_login["password"], password):
                flash("You have successfully login.")
                session["user"] = user_login["name"]
                session["user_id"] = user_login["user_id"]
                return redirect(url_for('index'))
            else:
                flash("Invalid password. Please try again.")
                return redirect(url_for('login'))
    else:
        return render_template("login.html")
    
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        hash_password = generate_password_hash(password)
        sql_query = f"INSERT INTO Users (name, password) VALUES ('{username}', '{hash_password}')"

        cursor = mysql.connection.cursor()
        cursor.execute(sql_query)
        mysql.connection.commit()
        flash("Registration is succesful. Please login.")
        return redirect(url_for('login'))
    else:
        return render_template("register.html")
    
@app.route("/validate", methods=["GET"]) 
def validate():
    """Return true if username available, else false, in JSON format"""
    
    username = request.args.get('username')
    
    if username == "":
        return jsonify({"status":""})

    # check whether if the username contains "" or ' at the start and end of string
    # if yes, prompt the user to choose another username
    if ((username.startswith("\'")) or (username.startswith("\"")) or (username.endswith("\"")) or (username.endswith("\'"))
    or (username.startswith("\'") and username.endswith("\'")) or (username.startswith("\"") and username.endswith("\"")) 
    or (username.startswith("\'") and username.endswith("\"")) or (username.startswith("\"") and username.endswith("\'"))):
        return jsonify({"status":"invalid"})
    
    else:
        # Query database to check whether username exist
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT user_id, name, password FROM Users WHERE name=''' + "\'" + username + "\'")
        validate_user = cursor.fetchone()
            
        if validate_user:
            return jsonify({"status":"taken"})
        else:
            return jsonify({"status":"available"})
        
@app.route('/query', methods=["GET"])
def query():
    
    item_selected = request.args.get('item')

    # Query for all the menu items in the Menu table
    cursor = mysql.connection.cursor()

    cursor.execute('''SELECT calories, protein, fat, sodium, fiber, carbohydrates, sugars, potassium, vitamins FROM Cereals WHERE name=''' + "\'" + item_selected + "\'")
    
    cereal = cursor.fetchall();
    
    return jsonify({"cereal":cereal})

@app.route('/search', methods=["GET", "POST"])
def search():
    if "user" in session:
        if request.method == "POST":
            
            cursor = mysql.connection.cursor()
            
            selectedOption = request.form.get('selectOption')
            
            if selectedOption == "manufacturer":
                manufacturer_name = request.form.get('manufacturer_selection')
                cursor.execute('''SELECT Cereals.name, Cereals.calories, Manufacturer.manufacturer_description, Type.cereals_type FROM Cereals INNER JOIN Manufacturer ON Cereals.manufacturer_id =
                    Manufacturer.manufacturer_id INNER JOIN Type ON Cereals.type_id = Type.type_id WHERE Manufacturer.manufacturer_description=''' + "\'" + manufacturer_name + "\'")
                        
            elif selectedOption == "cereal_type":
                cereal_type = request.form.get("cereal_type_selection")
                cursor.execute('''SELECT Cereals.name, Cereals.calories, Manufacturer.manufacturer_description, Type.cereals_type FROM Cereals INNER JOIN Manufacturer ON Cereals.manufacturer_id =
                    Manufacturer.manufacturer_id INNER JOIN Type ON Cereals.type_id = Type.type_id WHERE Type.cereals_type=''' + "\'" + cereal_type + "\'")
                
            elif selectedOption == "cereal_name":
                cereal_name = request.form.get("cereal-name-input")
                cursor.execute('''SELECT Cereals.name, Cereals.calories, Manufacturer.manufacturer_description, Type.cereals_type FROM Cereals INNER JOIN Manufacturer ON Cereals.manufacturer_id =
                    Manufacturer.manufacturer_id INNER JOIN Type ON Cereals.type_id = Type.type_id WHERE Cereals.name=''' + "\'" + cereal_name + "\'")
            
            elif selectedOption  == "calories":
                calories_option_selection = request.form.get("calories_selection")
                calories_consumption = int(calories_option_selection[-3:])
                
                if calories_option_selection == "Above and include 100":
                    cursor.execute(f"SELECT Cereals.name, Cereals.calories, Manufacturer.manufacturer_description, Type.cereals_type FROM Cereals INNER JOIN Manufacturer ON Cereals.manufacturer_id = Manufacturer.manufacturer_id INNER JOIN Type ON Cereals.type_id = Type.type_id WHERE Cereals.calories>={calories_consumption}")
                                   
                elif calories_option_selection == "Below 100":
                    cursor.execute(f"SELECT Cereals.name, Cereals.calories, Manufacturer.manufacturer_description, Type.cereals_type FROM Cereals INNER JOIN Manufacturer ON Cereals.manufacturer_id = Manufacturer.manufacturer_id INNER JOIN Type ON Cereals.type_id = Type.type_id WHERE Cereals.calories<{calories_consumption}")   


            filtered_record = cursor.fetchall()
            
            row_return = len(filtered_record)
            
            return render_template("list.html", row_return=row_return, filtered_record=filtered_record)
        else:
            return render_template('search.html')
    else:
        flash("Please login first.")
        return redirect(url_for('login'))
    
# to be commit 311219
@app.route("/contributecheck", methods=["GET"])
def contributecheck():
    manufacturer = request.form.get("manufacturer_option_selection")
    new_manufacturer_name = request.form.get("new_manufacturer")
    cereal = request.form.get("cereal_name")
    
    if manufacturer == "Others":
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT manufacturer_description FROM Manufacturer WHERE manufacturer_description =''' + "\'" + new_manufacturer_name + "\'")     
        manufacturer_check_result = cursor.fetchone()
        
        if manufacturer_check_result:
            return jsonify({"mfr_name_status":"taken"})
        else:
            cursor.execute('''SELECT name FROM Cereals WHERE name=''' + "\'" + cereal + "\'")
            cereal_check_result = cursor.fetchone()
            
            if cereal_check_result:
                return jsonify({"mfr_name_status":"available", "cereal_name_status":"taken"})
            else:
                return jsonify({"mfr_name_status":"available", "cereal_name_status":"available"})
    else:
        cursor.execute('''SELECT name FROM Cereals WHERE name=''' + "\'" + cereal + "\'")
        cereal_check_result = cursor.fetchone()            
        if cereal_check_result:
            return jsonify({"cereal_name_status":"taken"})
        else:
            return jsonify({"cereal_name_status":"available"})
        
        
        
        
# to be commit 311219
@app.route("/contribute", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        manufacturer_option_selected = request.form.get("manufacturer_option_selection")
        cereal_name_submitted = request.form.get("cereal_name")
        cereal_type_id = int(float(request.form.get("cereal_option_list")))
        calories = int(float(request.form.get("calories")))
        protein = int(float(request.form.get("protein")))
        fat = int(float(request.form.get("fat")))
        sodium = int(float(request.form.get("sodium")))
        fiber = int(float(request.form.get("fiber")))
        carbohydrates = int(float(request.form.get("carbohydrates")))
        sugars = int(float(request.form.get("sugars")))
        potassium = int(float(request.form.get("potassium")))
        vitamins = int(float(request.form.get("vitamins")))
    
        if manufacturer_option_selected != "Others":
            mfr_id = int(manufacturer_option_selected)
            
            # Insert new cereal into cereals table
            cereal_sql_query = f"INSERT INTO Cereals (name, manufacturer_id, type_id, calories, protein, fat, sodium, fiber, carbohydrates, sugars, potassium, vitamins) VALUES ('{cereal_name_submitted}', {mfr_id}, {cereal_type_id}, {calories}, {protein}, {fat}, {sodium}, {fiber}, {carbohydrates}, {sugars}, {potassium}, {vitamins})"
            cursor = mysql.connection.cursor()
            cursor.execute(cereal_sql_query)
            mysql.connection.commit()
 
            # Update contribute table if above is new cereal name and manufacturer are successfully added to the Cereals and Manufacturer table
            # Get cereal_id from Cereals table
            cereal_id_query = cursor.execute('''SELECT cereal_id FROM Cereals WHERE name =''' + "\'" + cereal_name_submitted + "\'")            
            cereal_id = (cursor.fetchone())['cereal_id']
            
            contribute_sql_query = f"INSERT INTO Contribute (user_id, manufacturer_id, cereal_id) VALUES ({session['user_id']}, {mfr_id}, {cereal_id})"
            cursor.execute(contribute_sql_query)
            mysql.connection.commit()
            
            flash("Successully submitted a new manufacturer and a cereal brand to the database.")     
            
            return redirect(url_for('index')) 
        
        elif manufacturer_option_selected == "Others":
            new_manufacturer = request.form.get("new_manufacturer")
            
            # create the new manufacurer in the manufacturer table first    
            sql_query = f"INSERT INTO Manufacturer (manufacturer_description) VALUES ('{new_manufacturer}')"
            cursor = mysql.connection.cursor()
            cursor.execute(sql_query)
            mysql.connection.commit()
            
            # Get manufacturer id from manufacturer table
            cursor.execute('''SELECT manufacturer_id FROM Manufacturer WHERE manufacturer_description =''' + "\'" + new_manufacturer + "\'")

            mfr_id = (cursor.fetchone())['manufacturer_id']

            # Insert new cereal into Cereals table 
            cereal_sql_query = f"INSERT INTO Cereals (name, manufacturer_id, type_id, calories, protein, fat, sodium, fiber, carbohydrates, sugars, potassium, vitamins) VALUES ('{cereal_name_submitted}', {mfr_id}, {cereal_type_id}, {calories}, {protein}, {fat}, {sodium}, {fiber}, {carbohydrates}, {sugars}, {potassium}, {vitamins})"
            cursor.execute(cereal_sql_query)
            mysql.connection.commit()
            
            # Update contribute table if above is new cereal name and manufacturer are successfully added to the Cereals and Manufacturer table
            # Get cereal_id from Cereals table
            cereal_id_query = cursor.execute('''SELECT cereal_id FROM Cereals WHERE name =''' + "\'" + cereal_name_submitted + "\'")            
            cereal_id = (cursor.fetchone())['cereal_id']
            
            contribute_sql_query = f"INSERT INTO Contribute (user_id, manufacturer_id, cereal_id) VALUES ({session['user_id']}, {mfr_id}, {cereal_id})"
            cursor.execute(contribute_sql_query)
            mysql.connection.commit()
            
            flash("Successully submitted a new manufacturer and a cereal brand to the database.")
            
            return redirect(url_for('index'))
                           
    else:
        cursor = mysql.connection.cursor()

        cursor.execute(('''SELECT Manufacturer.manufacturer_description FROM Manufacturer''')) 
        
        cereal_manufacturer = cursor.fetchall();
        
        # Store the cereal manufacturer into a list
        cereal_manufacturer_list = []
        
        for item in range(len(cereal_manufacturer)):
            cereal_manufacturer_list.append(cereal_manufacturer[item]['manufacturer_description'])
    
        # cereal manufacturer list length
        cereal_manufacturer_list_length = len(cereal_manufacturer_list)
    
        return render_template("contribute.html", cereal_manufacturer_list=cereal_manufacturer_list, cereal_manufacturer_list_length=cereal_manufacturer_list_length)
    
@app.route("/logout")
def logout():
    if "user" in session:
        session.clear()
        flash("You have successfully logout.")
        return redirect(url_for('login'))
    else:
        flash("Please login first.")
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)