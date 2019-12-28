import os

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
app.config['MYSQL_USER'] = 'sql12317054'
app.config['MYSQL_PASSWORD'] = 'i4HZtC2C6y'
app.config['MYSQL_HOST'] = 'sql12.freemysqlhosting.net'
app.config['MYSQL_DB'] = 'sql12317054'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# Index Page
@app.route('/', methods=["GET", "POST"])
def index():
    # if request.method == "POST":
        # Query for all the cereal items in the Cereals table
    cursor = mysql.connection.cursor()

    cursor.execute(('''SELECT Cereals.name, manufacturer_description, Type.cereals_type,
            Cereals.protein, Cereals.fat, Cereals.sodium, Cereals.fiber, Cereals.carbohydrates, Cereals.sugars,
            Cereals.potassium, Cereals.vitamins, Cereals.ratings FROM Cereals INNER JOIN Manufacturer ON Cereals.manufacturer_id =
            Manufacturer.manufacturer_id INNER JOIN Type ON Cereals.type_id = Type.type_id ORDER BY Cereals.ratings DESC'''))

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
    
    # else:
    # return 'YAY'
    
@app.route('/query', methods=["GET"])
def query():
    
    item_selected = request.args.get('item')

    # Query for all the menu items in the Menu table
    cursor = mysql.connection.cursor()

    cursor.execute('''SELECT calories, protein, fat, sodium, fiber, carbohydrates, sugars, potassium, vitamins FROM Cereals WHERE name=''' + "\'" + item_selected + "\'")
    
    cereal = cursor.fetchall();
    
    return jsonify({"cereal":cereal})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)