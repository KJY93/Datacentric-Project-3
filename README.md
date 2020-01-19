# Milestone Project 3: Data Centric Development

## Cereal 101
### Introduction
This project focuses on the development of a web application that allows user to look up for nutritional information for a particular cereal, rate for their favourite cereals, contribute nutritional information of new cereals to the database and also to update / delete cereals ratings or nutritional information of a particular cereal they have submitted to the database previously. 

## Demo
Heroku Link: [Click Here](https://kjy-cereal-share.herokuapp.com/)
Screencast Link: [Click Here](https://www.screencast.com/t/MFqgdgxx)

## Personal Touch
- Added login / logout and register function in the web application
- Using AJAX jQuery to validate username availability before allowing user to sign up for an account
- Using AJAX jQuery to validate whether cereals and manufacturer has already exist in the database. This check will help to prevent duplication of records being enter to the database. 

## Project Strategy and Scope
### User Stories
1. User would like to search for nutritional information of a cereal based on manufacturer, cereals type(i.e. hot or cold), cereals name or calories of the cereals.
Feature to implement: To include a search form that allows user to begin their search by selecting either the manufacturer, cereals type, cereals name or the calories radiobutton.

2. User would like to give ratings and reviews for their favourite cereals.
Feature to implement: To include a rating form that allows user to provide ratings and review of a particular cereal of their choices.

3. User would like to contribute nutritional information of a new cereal.
Feature to implement: To include a contribute form that allows user to contribute new cereals with its associated nutritional information to the cereals database.

4. User would like to know the current top 3 cereals with the highest calories.
Feature to implement: To include a bar chart to display to users the top 3 cereals with the highest calories.

5. User would like to have an overview of a breakdown of cereals by manufacturer
Feature to implement: To include a doughnut chart to display to users the breakdown of cereals by manufacturer currently in the database.

6. User would like to have a quick overview of the detailed nutritional information of a particular cereals and manufacturer brand
Feature to implement: To include a search form that uses AJAX to retrieve relevant information from the database and display it back to the user.

7. User would like to update or delete their ratings for a particular cereal
Feature to implement: To include a user history page specific to that particular user that allows them to choose which cereals ratings that they would like to update or delete.

8. User would like to update or delete the cereals nutritional information
Feature to implement: To include a user history page specific to that particular user that allows them to choose which previous cereals contribution that they would like to update or delete.

## Project Structure
There are 3 main parts of this web application, i.e. user logging in / out, user registration and users accessing the web application features once they are logged in.

At the login page, existing user will need to login before they can access the in-app features of the web application. For new users, they will be redirected to the registration page to sign up for an account. 

Logged out features are only allowed for users which are currently logged in.

Once users are logged in, they will be redirected to the landing page, which comprise of the navbar at the uppermost part of the web application. The navbar contains link to the search, contribute, history and logout page.

On the index page, users will be provided with an overview of the number of current records in the database, an overview of the cereal brands by manufacturer, a barchart comparing the top 3 cereals with the highest calories and an autocomplete search form that allows user to query for the nutritional information for a particular cereals.

On the search page, users will be able to search for a particular cereals based on one of the following options: manufacturer, cereals type, cereal name and calories. Results returned will be displayed in table format and when user clicks on the cereal name in the table they will be redirected to the ratings and reviews page.

On the history page, users will be able to view their own previous ratings or cereals contribution by clicking on either the ratings info or cereals info radiobutton. Upon clicking on either one of the selection, users will be redirected to the page whereby they will be allowed to edit or delete the ratings or contributions they have made previously.

Clicking on the logout button will logged the user out and clear the session related to that particular user.

### a. Wireframes
https://drive.google.com/open?id=1-gI9QTKHP6YpJK-H2sbTUpM3gq-yeiJE

### b. ER diagram
ER diagram was used for the database design. There are 5 tables that has been identified during the database design stage. The 5 tables and their relationships between each other are as below:

a. Tables: Cereals, Manufacturer, Type, Contribute, Users

b. Entity Relationship (ER) diagram:
![ER diagram](https://www.lucidchart.com/publicSegments/view/dcf7bc02-6eb6-4d83-a963-05e196842fa7/image.jpeg)

Note: PK (Primary Key), FK (Foreign Key)

## Project Skeleton
### a. Existing Features
a. Application was designed with Bootstrap grid design and mobile responsiveness in mind. 
b. New user is able to sign up for a new account.
c. Users are able to login and logout of the web application.
d. Users are able to give reviews and ratings to their favourite cereals.
e. Users are able to update or delete their previous cereals ratings but are not allowed to create duplicate ratings and reviews for the same cereals. 
f. Users are able to contribute new cereal nutritional information to the database.
g. Users are able to update or delete their previous cereal contribution.
h. Users are able to search for cereals information by either the manufacturer, cereals type, cereal name or amount of calories.
i. Users are able to view their own previous cereals ratings and cereal contributions.

### b. Features to be implemented in the future
a. For the future development of this cereal nutritional information web application, I would like to include the following features:
   * Allow user to upload images for different brand of cereals
   * Allow user to have followers
   * ALlow user to share their favourite cereals with their followers
   * Implement the return to previous page button

## Project Surface
Design Choices:
1. This web application was designed in a way such that it gives a dashboard like kind of feel.
2. Charts are used to gives the users a visual representation of the nutritional information for a particular cereals.
3. Modal form is used to display relevant information based on what radiobuttons the user has clicked on.
4. Slackey, a chuncky and entertaining font was used to display the texts used in this web application.

## Technologies used
1. HTML5 was the markup language used for structuring the content of the web application
2. CSS3 was a style sheet language used to format the outlook of the web application
3. JavaScript was the programming language to add front end interactivity to the web application
4. jQuery is a JavaScript library. It was used to manipulate the HTML DOM element, event handling, animation and AJAX - https://jquery.com/
5. Bootstrap 4 was the framework used to make the application responsive - https://getbootstrap.com/
6. Heroku was used to deploy the web application    
7. ChartJS was used to plot the charts found in the web application - https://www.chartjs.org/
8. ChartJS plugins was used to display the labelling for the doughnut chart - https://github.com/emn178/chartjs-plugin-labels 
9. Heroku ClearDB was used as the MySQL database to store all the datatables and datasets
10. HeidiSQL was used to view the structures and datasets in the database -  https://www.heidisql.com/
11. Twitter typeahead.js and BloodHound was used to incorporate the autocomplete function in the search form- https://github.com/twitter/typeahead.js
12. Python was used as the backend to write up the different routes to handle the different request method
13. Flask-MySQLdb was used to connect Flask with MySQL
14. LucidChart was used to tool up the ER diagram for the database design - https://www.lucidchart.com/

## Testing (Manual)
### Responsiveness
The web application was tested across multiple device screen sizes (small: iPhone 5, Galaxy S5, Pixel 2, medium: iPad, large: iPad Pro). Website scale responsively according to the device screen when tested in the Developer tools.

### Browser compatibility
The web application was tested and is compatible on Chrome, Opera and Firefox.

### Test Cases
| Test Case     | Description                   | Outcome  |
| ------------- |-----------------------------  | -------- |
|1              | New users will be redirected to the register page if they try to login with a username that does not exist. At the same time, a flash messages will also appear to notify the user that they need to have an account before they are allowed to user the in-app feature of the web application. | Pass     |
|2              | New users can only register with a username that does not exist in the Users table in the database. If no record is found, user will be allowed to register with the username that they have key in and a message will be popped up notifying the user that they have successfully registered for an account. | Pass     |
|3              | New users must provide a strong enough password during account registration, i.e. password must contain alphanumeric characters and special symbols(!@#$%^&*) and be 8 to 15 characters long. If password provided does not fulfill the password requirement criteria, an alert message will popped up to notify the user and the registration form will not be submitted to the backend for further processing. | Pass     |
|4              | Password and repeated password fields must be the same to register for a new user account. Else, an alert message will be popped up to notify the user that they have a mismatch password fields. | Pass     |
|5              | Upon logging in to the web application, users will reach the landing page whereby users will see a navbar on the top part of the website (which includes the contribute, search, history and logout tab). At the body section of the web application, users will be able to see a message at the top letting users know how many records are there currently in the database, a doughnut chart showing the breakdown of cereals by manufacturer, top 3 cereals with highest calories and an autocomplete search form that allows user to search for nutritional information of a particular cereal. | Pass     |
|6              | Upon clicking on the contribute tab of the navbar, users will be able to contribute new cereals information by filling up the form. If users select the "Others" option for the manufacturer category, users will need to provide a new name for the manufacturer. This new name will be checked against the Manufacturer table in the database. If it is found that the manufacturer name exist, the users will not be allowed to add that particular manufacturer to the database. | Pass     |
|7              | Upon clicking on the search tab of the navbar, users will be able to search for a particular cereals by manufacturer, cereals type, cereals name or calories. The results will be displayed in a table format based on the selection made. In the table, user will be able to see a summary of the cereals which includes the cereal name, manufacturer, cereal type and calories. If the user clicks on the cereal name, they will be redirected to the ratings page that allows them to give their reviews and ratings for that particular cereal. | Pass     |
|8              | Upon clicking on the history tab of the navbar, users will be brought to the history page whereby they will need to choose either the ratings info or the cereals info radiobutton. When clicked on the ratings info radiobutton, user will be shown the previous ratings that they can edit or delete. When clicked on the cereal info radiobutton, user will be shown the previous cereals contribution they can update or delete. | Pass     |
|9              | If user choose to edit the previous ratings or cereal contribution, the edit form will be popped up with information that they have submitted previously from the database. | Pass     |
|10             | Messages will be flashed up whenever the user has successfully added, deleted or removed a record from the database. | Pass     |
|11             | Flashed messages is made to disappear after a certain time lapse using jQuery fadeOut function. | Pass     |
|12             | When user clicks on logout, they will be logged out from the web application and the session related to the particular user will be cleared. | Pass     |
|13             | User will be shown the ratings and contributions specific to them when they clicked on the history tab. This allows only the rightful owner perform the editing or deleting action of a record from the database. | Pass     |
|14             | Users are able to login only if the correct username and password is provided. Else an error message of invalid username / password will be shown to the user. | Pass     |

## Files Description
The files used in this web application are briefly described as below:
1. app.py - the backend Python file that is used to handle the different routes for this web application
2. csv files - the datasets that is to be imported to the database using Python script
3. create_datatables.py - Python script to automatically create the datatables needed in the database
4. import_datasets.py - Python script to automatically import the datasets in the csv file (item no.2) to the datatables in the database
5. templates - templates folder contains all the html files for this web application
6. static folder contains 3 sub folders, namely static, images and scripts. Static folder contains the external CSS file while images and scripts folder contains the images and external JavaScript files used in this web application respectively
7. requirements.txt - the text files that contains all the packages needed to run this web application

## How to Login and Sign Up For An Account
a. New User
1. New user will need to signup for an account at the registration page before using the web application
2. New user will need to provide their own username. It the username is already taken, an alert message will appear to notify them to choose another username.
3. Password provided need to contain alphanumeric characters and special symbols(!@#$%^&*) and be 8 to 15 characters long.

An example of the login username and password would be:
1. Username: admin
2. Password: @Admin12345

b. Existing User
1. Existing user would need to login at the login page using their own username and password. An alert message will appear if the user has provide a wrong username or password.

## Bugs and Limitations Discovered
jQuery was used to update the cereal info edit form under the history tab. 
The manufacturer and cereal type in the edit form is correctly selected on laptop and desktop but not on mobile device.
Upon checking the Internet, it seems like jQuery has some compability issue with mobile device.

Snapshot of limitations discovered:
- Laptop have the correct manufacturer and cereals type selected (left picture)
- Mobile device does not have the correct manufacturer and cereals type selected (right picture)

Laptop / Desktop                                        |  Mobile Device
:------------------------------------------------------:|:-----------------------------------------------------:
![display on laptop](https://i.imgur.com/8gbf1JH.png)   | ![display on mobile](https://i.imgur.com/8DjpwOQ.png)

## Deployment
### a. Setting up MySQL (ClearDB) with Heroku
1. Installing ClearDB in Git Bash using ```heroku addons:create cleardb:ignite```
2. Datatables in the database were created using the create_datatables.py file written by the developer
3. Datasets were imported automatically from the csv file using import_datasets.py file written by the developer

### b. Heroku Deployment
1. Sign up for an account at [Heroku](https://www.heroku.com/).
2. Download Heroku CLI at [Heroku](https://devcenter.heroku.com/articles/heroku-cli#download-and-install) website.
3. Install the dowloaded Heroku CLI from Step 2.
4. Open up Git Bash terminal. Cd to the location that you have your project in. Then, in the Git Bash Terminal, login to Heroku by typing ```heroku login```. A login page will be popped up to allow you to login to Heroku.
5. Open up another Git Bash terminal. Create a new app using ```heroku create <app_name>```.
6. In Git Bash, check whether the new remotes has been successfully added using ```git remote -v```.
7. In Git Bash, install gunicorn with the command ```git remote -v```.
8. Create a file called Procfile. Add ```web gunicorn app:app``` and save it.
9. Create the requirements.txt file with ```pip3 freeze --local > requirements.txt```.
10. In Git Bash, commit and push the project to GitHub and Heroku with the following:
* ```git add .```
* ```git commit -m "<Commit Message>"```
* ```git push heroku master```
11. In Heroku, set up your key and value pair needed for the project. For this project, the database url, MySQL username, database, host and password has been configured under the Settings Tab.
12. To open up the app hosted on Heroku, click on the "Open App" button at the very top page of the Heroku dashboard.

### b. To run this web application on your local PC
Instructions
Note: This web application was run on a Windows PC. The following command might be slightly different if run on a Mac PC.

1. Go to [Cereal 101 github repository](https://github.com/KJY93/Datacentric-Project-3).
   
2. Click on the 'Clone or Download' button and then click 'Download ZIP' and extract the files to a location of your choice on your laptop / desktop. Else, you can clone the project by running the following command on your terminal:
```git clone https://github.com/<username>/<repository>```

3. Create a virtual environment using the following command:
```python -m venv venv```  

4. Activate the virtual environment created using the following command:
On Windows: ```venv\Scripts\activate``` 

5. Install all the packages needed using the following command:
```pip install -r requirements.txt```

6. Set the enviroment variables needed to run this web application. First, right click on ```My Computer```. Then right click on ```Properties```. On the left hand side of the menu bar, click on ```Advanced system settings```. Under the ```System Variables``` section, click on the ```New``` button. In the pop up dialog box, key in the ```Variable Name``` and ```Variable Value``` field. The environment variables needed to be setup would be the database name, database host, database password and database username.
Note: For the variable name, you are free to choose a variable name of your choice:

An example of the enviroment variables key values pair would be as follow:
a. MYSQL_HOST(variable name) will be: us-cdbr-iron-east-02.cleardb.net (variable value)
b. MYSQL_USER(variable name) will be: B80f8d428xxxxx(variable value)
c. MYSQL_PASSWORD(variable name) will be: F48exxxx(variable value)
d. MYSQL_DB will(variable name) be: heroku_58632fb6debxxxx(variable value)

7. Run the application using the following command:
```python app.py```

8. To see the web application in action, go the the following link:
```http://127.0.0.1:8080```  

### Credits and Acknowledgements:
1. Twitter typeahead.js: 
   Source code to implement the autocomplete search feature in the search form adapted from https://github.com/twitter/typeahead.js

2. Font Awesome:
   Icons from Font Awesome were used to style the edit and delete button for the update / delete ratings and cereal contribution form - https://fontawesome.com/

3. Fonts: 
   Font used is from https://fonts.google.com/

4. Icons8:
   Logo from favicon is used as the logo for the tab browser of this web application - https://icons8.com/

5. ChartJS plugin:
   ChartJS plugin is used to display the labelling on the doughnut chart - https://cdn.jsdelivr.net/gh/emn178/chartjs-plugin-labels/src/chartjs-plugin-labels.js

6. Kaggle:
   Cereal nutritional datasets used for this web application - https://www.kaggle.com/crawford/80-cereals

7. Datatables.net
   Advanced interaction controls for HTML tables - https://datatables.net/

8. Colors used for the charts:
   The idea to represent the different colors on the doughnut chart was adapted from this site - https://mika-s.github.io/javascript/colors/hsl/2017/12/05/generating-random-colors-in-javascript.html

Note: This is for educational purpose only and not for commercial use.