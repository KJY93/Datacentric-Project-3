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

# Setting up the configurations needed to access the MySQL database
app.config['MYSQL_USER'] = os.environ.get("MYSQL_USER")
app.config['MYSQL_PASSWORD'] = os.environ.get("MYSQL_PASSWORD")
app.config['MYSQL_HOST'] = os.environ.get("MYSQL_HOST")
app.config['MYSQL_DB'] = os.environ.get("MYSQL_DB")
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
        
        # close the connection when finish the querying
        cursor.close()

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

        cursor.execute(
            '''SELECT user_id, name, password FROM Users WHERE name=''' + "\'" + name + "\'")

        user_login = cursor.fetchone()

        if user_login == None:
            flash("Username does not exist. Please register.")
            return redirect(url_for('register'))

        elif len(user_login) != 0:
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
        return jsonify({"status": ""})

    # check whether if the username contains "" or ' at the start and end of string
    # if yes, prompt the user to choose another username
    if ((username.startswith("\'")) or (username.startswith("\"")) or (username.endswith("\"")) or (username.endswith("\'"))
        or (username.startswith("\'") and username.endswith("\'")) or (username.startswith("\"") and username.endswith("\""))
            or (username.startswith("\'") and username.endswith("\"")) or (username.startswith("\"") and username.endswith("\'"))):
        return jsonify({"status": "invalid"})

    else:
        # Query database to check whether username exist
        cursor = mysql.connection.cursor()
        cursor.execute(
            '''SELECT user_id, name, password FROM Users WHERE name=''' + "\'" + username + "\'")
        validate_user = cursor.fetchone()

        if validate_user:
            return jsonify({"status": "taken"})
        else:
            return jsonify({"status": "available"})

@app.route('/query', methods=["GET"])
def query():

    item_selected = request.args.get('item')

    # Query for all the menu items in the Menu table
    cursor = mysql.connection.cursor()

    cursor.execute('''SELECT calories, protein, fat, sodium, fiber, carbohydrates, sugars, potassium, vitamins FROM Cereals WHERE name=''' + "\'" + item_selected + "\'")

    cereal = cursor.fetchall()
    
    # close the connection when finish the querying
    cursor.close()

    return jsonify({"cereal": cereal})

@app.route('/search', methods=["GET", "POST"])
def search():
    if "user" in session:
        if request.method == "POST":

            cursor = mysql.connection.cursor()

            selectedOption = request.form.get('selectOption')

            if selectedOption == "manufacturer":
                manufacturer_name = request.form.get('manufacturer_selection')
                cursor.execute('''SELECT Cereals.cereal_id, Cereals.name, Cereals.calories, Manufacturer.manufacturer_description, Type.cereals_type FROM Cereals INNER JOIN Manufacturer ON Cereals.manufacturer_id =
                    Manufacturer.manufacturer_id INNER JOIN Type ON Cereals.type_id = Type.type_id WHERE Manufacturer.manufacturer_description=''' + "\'" + manufacturer_name + "\'")

            elif selectedOption == "cereal_type":
                cereal_type = request.form.get("cereal_type_selection")
                cursor.execute('''SELECT Cereals.cereal_id, Cereals.name, Cereals.calories, Manufacturer.manufacturer_description, Type.cereals_type FROM Cereals INNER JOIN Manufacturer ON Cereals.manufacturer_id =
                    Manufacturer.manufacturer_id INNER JOIN Type ON Cereals.type_id = Type.type_id WHERE Type.cereals_type=''' + "\'" + cereal_type + "\'")

            elif selectedOption == "cereal_name":
                cereal_name = request.form.get("cereal-name-input")
                cursor.execute('''SELECT Cereals.cereal_id, Cereals.name, Cereals.calories, Manufacturer.manufacturer_description, Type.cereals_type FROM Cereals INNER JOIN Manufacturer ON Cereals.manufacturer_id =
                    Manufacturer.manufacturer_id INNER JOIN Type ON Cereals.type_id = Type.type_id WHERE Cereals.name=''' + "\'" + cereal_name + "\'")

            elif selectedOption == "calories":
                calories_option_selection = request.form.get(
                    "calories_selection")
                calories_consumption = int(calories_option_selection[-3:])

                if calories_option_selection == "Above and include 100":
                    cursor.execute(
                        f"SELECT Cereals.cereal_id, Cereals.name, Cereals.calories, Manufacturer.manufacturer_description, Type.cereals_type FROM Cereals INNER JOIN Manufacturer ON Cereals.manufacturer_id = Manufacturer.manufacturer_id INNER JOIN Type ON Cereals.type_id = Type.type_id WHERE Cereals.calories>={calories_consumption}")

                elif calories_option_selection == "Below 100":
                    cursor.execute(
                        f"SELECT Cereals.cereal_id, Cereals.name, Cereals.calories, Manufacturer.manufacturer_description, Type.cereals_type FROM Cereals INNER JOIN Manufacturer ON Cereals.manufacturer_id = Manufacturer.manufacturer_id INNER JOIN Type ON Cereals.type_id = Type.type_id WHERE Cereals.calories<{calories_consumption}")

            filtered_record = cursor.fetchall()
            
            row_return = len(filtered_record)
            
            # close the connection when finish the querying
            cursor.close()

            return render_template("list.html", row_return=row_return, filtered_record=filtered_record)
        else:
            return render_template('search.html')
    else:
        flash("Please login first.")
        return redirect(url_for('login'))

@app.route("/contributecheck", methods=["GET"])
def contributecheck():

    # lowercase and then capitalize only the first letter of the string before perform the sql query
    cereal = request.args.get('cereal')
    cereal_lowercase = cereal.lower()
    cereal_formatted = ' '.join(elem[0].upper() + elem[1:] for elem in cereal_lowercase.split())

    manufacturer = request.args.get('manufacturer')
    cursor = mysql.connection.cursor()

    if manufacturer == "Others":
        new_manufacturer = request.args.get('new_mfr')

        # lowercase and then capitalize only the first letter of the string before perform the sql query
        # this is needed to ensure no duplicates names are being entered to the database
        lower_case_new_manufacturer = new_manufacturer.lower()
        capitalize_new_manufacturer = ' '.join(
            word[0].upper() + word[1:] for word in lower_case_new_manufacturer.split())

        cursor.execute('''SELECT manufacturer_description FROM Manufacturer WHERE manufacturer_description =''' +
                       "\'" + capitalize_new_manufacturer + "\'")

        manufacturer_check_result = cursor.fetchone()

        if manufacturer_check_result:
            return jsonify({"mfr_name_status": "taken"})
        else:
            cursor.execute(
                '''SELECT name FROM Cereals WHERE name=''' + "\'" + cereal_formatted + "\'")
            cereal_check_result = cursor.fetchone()
            
            # close the connection when finish the querying
            cursor.close()

            if cereal_check_result:
                return jsonify({"mfr_name_status": "available", "cereal_name_status": "taken"})
            else:
                return jsonify({"mfr_name_status": "available", "cereal_name_status": "available"})
    else:
        cursor.execute('''SELECT name FROM Cereals WHERE name=''' +
                       "\'" + cereal_formatted + "\'")
        cereal_check_result = cursor.fetchone()

        # close the connection when finish the querying
        cursor.close()
        
        if cereal_check_result:
            return jsonify({"cereal_name_status": "taken"})
        else:
            return jsonify({"cereal_name_status": "available"})

@app.route("/contribute", methods=["GET", "POST"])
def contribute():
    if request.method == "POST":
        manufacturer_option_selected = request.form.get(
            "manufacturer_option_selection")

        # lowercase and then capitalize only the first letter of the string before perform the sql query
        # this is needed to ensure consistent formatting of names are being entered to the database
        cereal_name_submitted = request.form.get("cereal_name").lower()
        cereal_name_formatted = ' '.join(
            word[0].upper() + word[1:] for word in cereal_name_submitted.split())

        cereal_type_id = int(request.form.get("cereal_option_list"))
        calories = round(float(request.form.get("calories")))
        protein = round(float(request.form.get("protein")))
        fat = round(float(request.form.get("fat")))
        sodium = round(float(request.form.get("sodium")))
        fiber = round(float(request.form.get("fiber")))
        carbohydrates = round(float(request.form.get("carbohydrates")))
        sugars = round(float(request.form.get("sugars")))
        potassium = round(float(request.form.get("potassium")))
        vitamins = round(float(request.form.get("vitamins")))

        cursor = mysql.connection.cursor()

        if manufacturer_option_selected != "Others":
            # Get manufacturer id
            cursor.execute('''SELECT manufacturer_id FROM Manufacturer WHERE manufacturer_description=''' +
                           "\'" + manufacturer_option_selected + "\'")

            mfr_id = cursor.fetchone()["manufacturer_id"]

            # Insert new cereal into cereals table
            cereal_sql_query = f"INSERT INTO Cereals (name, manufacturer_id, type_id, calories, protein, fat, sodium, fiber, carbohydrates, sugars, potassium, vitamins) VALUES ('{cereal_name_formatted}', {mfr_id}, {cereal_type_id}, {calories}, {protein}, {fat}, {sodium}, {fiber}, {carbohydrates}, {sugars}, {potassium}, {vitamins})"
            cursor.execute(cereal_sql_query)
            mysql.connection.commit()

            # Update contribute table if above is new cereal name and manufacturer are successfully added to the Cereals and Manufacturer table
            # Get cereal_id from Cereals table
            cereal_id_query = cursor.execute(
                '''SELECT cereal_id FROM Cereals WHERE name =''' + "\'" + cereal_name_formatted + "\'")
            cereal_id = (cursor.fetchone())['cereal_id']

            contribute_sql_query = f"INSERT INTO Contribute (user_id, manufacturer_id, cereal_id) VALUES ({session['user_id']}, {mfr_id}, {cereal_id})"
            cursor.execute(contribute_sql_query)
            mysql.connection.commit()
            
            # close the connection when finish the querying
            cursor.close()

            flash("Successully submitted a cereal brand to the database.")

            return redirect(url_for('index'))

        elif manufacturer_option_selected == "Others":
            new_manufacturer = request.form.get("new_manufacturer")

            # lowercase and then capitalize only the first letter of the string before perform the sql query
            # this is needed to ensure consistent formatting of names are being entered to the database
            new_mfr_lowercase = new_manufacturer.lower()
            new_mfr_formatted = ' '.join(
                i[0].upper() + i[1:] for i in new_mfr_lowercase.split())

            # create the new manufacurer in the manufacturer table first
            sql_query = f"INSERT INTO Manufacturer (manufacturer_description) VALUES ('{new_mfr_formatted}')"
            cursor.execute(sql_query)
            mysql.connection.commit()

            # Get manufacturer id from manufacturer table
            cursor.execute(
                '''SELECT manufacturer_id FROM Manufacturer WHERE manufacturer_description =''' + "\'" + new_mfr_formatted + "\'")

            mfr_id = (cursor.fetchone())['manufacturer_id']

            # Insert new cereal into Cereals table
            cereal_sql_query = f"INSERT INTO Cereals (name, manufacturer_id, type_id, calories, protein, fat, sodium, fiber, carbohydrates, sugars, potassium, vitamins) VALUES ('{cereal_name_formatted}', {mfr_id}, {cereal_type_id}, {calories}, {protein}, {fat}, {sodium}, {fiber}, {carbohydrates}, {sugars}, {potassium}, {vitamins})"
            cursor.execute(cereal_sql_query)
            mysql.connection.commit()

            # Update contribute table if above is new cereal name and manufacturer are successfully added to the Cereals and Manufacturer table
            # Get cereal_id from Cereals table
            cereal_id_query = cursor.execute(
                '''SELECT cereal_id FROM Cereals WHERE name =''' + "\'" + cereal_name_formatted + "\'")
            cereal_id = (cursor.fetchone())['cereal_id']

            contribute_sql_query = f"INSERT INTO Contribute (user_id, manufacturer_id, cereal_id) VALUES ({session['user_id']}, {mfr_id}, {cereal_id})"
            cursor.execute(contribute_sql_query)
            mysql.connection.commit()

            # close the connection when finish the querying
            cursor.close()

            flash("Successully submitted a new manufacturer and a cereal brand to the database.")

        return redirect(url_for('index'))

    else:
        cursor = mysql.connection.cursor()

        cursor.execute(
            ('''SELECT Manufacturer.manufacturer_description FROM Manufacturer'''))

        cereal_manufacturer = cursor.fetchall()
        
        # close the connection when finish the querying
        cursor.close()

        # Store the cereal manufacturer into a list
        cereal_manufacturer_list = []

        for item in range(len(cereal_manufacturer)):
            cereal_manufacturer_list.append(
                cereal_manufacturer[item]['manufacturer_description'])

        # cereal manufacturer list length
        cereal_manufacturer_list_length = len(cereal_manufacturer_list)

        return render_template("contribute.html", cereal_manufacturer_list=cereal_manufacturer_list, cereal_manufacturer_list_length=cereal_manufacturer_list_length)
    
@app.route("/ratings/<int:cereal_id>", methods=["GET", "POST"])
def ratings(cereal_id):
    if "user" in session:
        cursor = mysql.connection.cursor()
        
        if request.method == "POST":
            user_comment = request.form.get("user_comment")
            
            # format the user comment (use "\\ to escape quotes to prevent sql injection")
            if user_comment.find("\'"):
                user_comment_formatted = user_comment.replace("\'", "’")
            elif user_comment.find("\""):
                user_comment_formatted = user_comment.replace("\"", "’")  
            
            
            user_ratings = round(float(request.form.get("user_ratings")), 2)
            uid = session["user_id"]
            cid = cereal_id
            
            # check whether user has rate a particular cereal
            # if yes, do not allow them to resubmit the a brand new rating for the same cereal
            # only update on the existing rating is allowed
            cursor.execute((f"SELECT cereal_id FROM Ratings WHERE cereal_id={cid} and user_id={uid}"))
            
            ratings_check = cursor.fetchone()
            
            if ratings_check:
                return render_template("error.html", message="Error message: Multiple reviews are not allowed.")
            else:
                ratings_query = f"INSERT INTO Ratings (ratings, comment, user_id, cereal_id) VALUES ({user_ratings}, '{user_comment_formatted}', {uid}, {cid})"                
                cursor.execute(ratings_query)
                mysql.connection.commit()
                
                # close the connection when finish the querying
                cursor.close()
        
                flash("You have successfully submit a rating.")
                return redirect(url_for('index'))    
        else:
            cursor.execute((f"SELECT Cereals.cereal_id, Cereals.name, manufacturer_description, Type.cereals_type, Cereals.calories FROM Cereals INNER JOIN Manufacturer ON Cereals.manufacturer_id = Manufacturer.manufacturer_id INNER JOIN Type ON Cereals.type_id = Type.type_id WHERE cereal_id={cereal_id}"))
            
            item_searched = cursor.fetchone()
            
            # close the connection when finish the querying
            cursor.close()

            return render_template("ratings.html", item_searched=item_searched)

    else:
        flash("Please login first.")
        return redirect(url_for('login'))
    
@app.route('/history', methods=["GET"])
def history():
    if "user" in session:
        cursor = mysql.connection.cursor()
        # Get the cereal ratings for the logged in user
        cursor.execute(f"SELECT Cereals.name, Cereals.cereal_id, Ratings.comment, Ratings.ratings FROM Ratings INNER JOIN Cereals ON Ratings.cereal_id = Cereals.cereal_id WHERE user_id={session['user_id']}")
        rating_query = cursor.fetchall()
        
        # Get the cereal info contributed by the logged in user
        cursor.execute(f"SELECT Cereals.name, Cereals.cereal_id, Manufacturer.manufacturer_id, Manufacturer.manufacturer_description FROM Contribute INNER JOIN Cereals ON Contribute.cereal_id = Cereals.cereal_id INNER JOIN Manufacturer ON Contribute.manufacturer_id = Manufacturer.manufacturer_id WHERE user_id={session['user_id']}")
        
        contribute_query = cursor.fetchall()
        
        # close the connection when finish the querying
        cursor.close()
        
        return render_template("history.html", rating_query=rating_query, contribute_query=contribute_query)
    else:
        flash("Please login first.")
        return redirect(url_for('login'))
    
@app.route('/editratings/<int:cereal_id>', methods=["POST"])
def editratings(cereal_id):
    cereal_ratings_update = round(float(request.form.get("user_ratings_update")), 2)
    cereal_comments_update = request.form.get("user_comment_update")
    
    cursor = mysql.connection.cursor()
    cursor.execute((f"SELECT cereal_id FROM Ratings WHERE cereal_id={cereal_id}"))
    
    cereal_update_query = cursor.fetchone()
    
    if cereal_update_query:
        cereal_updated = f"UPDATE Ratings SET ratings={cereal_ratings_update}, comment='{cereal_comments_update}' WHERE cereal_id={cereal_id} and user_id={session['user_id']}"
        cursor.execute(cereal_updated)
        mysql.connection.commit()
        
        # close the connection when finish the querying
        cursor.close()
        
        flash("Successfully updated your ratings review")
        return redirect(url_for('index'))
    else:
        # close the connection
        cursor.close()
        return render_template("error.html", message="Error message: No ratings for this cereal is found.")
    
@app.route('/deleteratings/<int:cereal_id>', methods=["POST"])
def deleteratings(cereal_id):
    
    cursor = mysql.connection.cursor()

    cereal_delete_query = f"DELETE FROM Ratings WHERE cereal_id={cereal_id} and user_id={session['user_id']}"
    cursor.execute(cereal_delete_query)
    mysql.connection.commit()
    
    # close the connection when finish the querying
    cursor.close()  
    
    flash("Successfully deleted your ratings review")
    return redirect(url_for('index'))

@app.route('/editcontribution/<int:cereal_id>', methods=["POST"])
def editcontribution(cereal_id):
    
    cursor = mysql.connection.cursor()
    
    # get previous mfr_id
    cursor.execute(f"SELECT manufacturer_id FROM Contribute WHERE cereal_id={cereal_id}")
    previous_mfr_id = int(cursor.fetchone()['manufacturer_id'])
    
    # get submitted mfr_id
    cursor.execute(f"SELECT manufacturer_id FROM Manufacturer WHERE manufacturer_description='{request.form.get('manufacturer_option_selection')}'")
    submitted_mfr_id = int(cursor.fetchone()['manufacturer_id'])
    
    
    print(request.form.get('manufacturer_option_selection'))
    # get submitted values from form
    cereal = request.form.get("cereal_name")
    cereal_type = int(request.form.get("cereal_option_list"))
    calories = round(float(request.form.get("calories")))
    protein = round(float(request.form.get("protein")))
    fat = round(float(request.form.get("fat")))
    sodium = round(float(request.form.get("sodium")))
    fiber = round(float(request.form.get("fiber")))
    carbohydrates = round(float(request.form.get("carbohydrates")))
    sugars = round(float(request.form.get("sugars")))
    potassium = round(float(request.form.get("potassium")))
    vitamins = round(float(request.form.get("vitamins")))
    
    # if previous mfr id is equal to the submitted mfr id, just update the cereals table
    if previous_mfr_id == submitted_mfr_id:
        cereal_query_update = f"UPDATE Cereals SET name='{cereal}', type_id={cereal_type}, calories={calories}, protein={protein}, fat={fat}, sodium={sodium}, fiber={fiber}, carbohydrates={carbohydrates}, sugars={sugars}, potassium={potassium}, vitamins={vitamins}  WHERE cereal_id={cereal_id}"
        cursor.execute(cereal_query_update)
        mysql.connection.commit()
        
        # close the connection when finish the querying
        cursor.close()
        
        flash("Successfully update cereal info.")
        return redirect(url_for('index'))
    
    # else update contribute table then cereals table
    elif previous_mfr_id != submitted_mfr_id:
        # update contribute table
        print("here")
        contribute_table_update = f"UPDATE Contribute SET manufacturer_id={submitted_mfr_id} WHERE cereal_id={cereal_id} and user_id={session['user_id']}"
        cursor.execute(contribute_table_update)
        mysql.connection.commit()
        
        cereal_query_update = f"UPDATE Cereals SET manufacturer_id={submitted_mfr_id}, name='{cereal}', type_id={cereal_type}, calories={calories}, protein={protein}, fat={fat}, sodium={sodium}, fiber={fiber}, carbohydrates={carbohydrates}, sugars={sugars}, potassium={potassium}, vitamins={vitamins}  WHERE cereal_id={cereal_id}"
        cursor.execute(cereal_query_update)
        mysql.connection.commit()
        
        # close the connection when finish the querying
        cursor.close()
        
        flash("Successfully update cereal info.")
        return redirect(url_for('index'))

    else:
        return render_template("error.html", message="Error message: An unknown error occured.")
    
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
