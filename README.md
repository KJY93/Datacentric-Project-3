# Milestone Project 3: Data Centric Development

## Cereal 101
### Introduction
This project focuses on the development of a web application that allows users to look up for nutritional information for a cereals of a particular brand, rate their favourite cereals and also to contribute nutritional information of a new cereals to the cereals database. 

## Demo

## Project Strategy and Scope
### User Stories
1. User would like to search for nutritional information of a cereals based on manufacturer, cereals type(i.e. hot or cold), cereals name or calories of the cereals.
Features to implement: To include a search form that allows user to begin their search by selecting either the manufacturer, cereals type, cereals name or the calories radiobutton.

2. User would like to give ratings and reviews for their favourite cereals.
Features to implement: To include a rating form that allows user to provide review of a particular cereals of their choices.

3. User would like to contribute nutritional information of a new cereals.
Features to implement: To include a contribute form that allows user to contribute new cereals with its associated nutritional information to the cereals database.

4. User would like to know the current top 3 cereals with the highest calories.
Features to implement: To include a bar chart to display to users the top 3 cereals with the highest calories.

5. User would like to have an overview of a breakdown of cereals by manufacturer
Features to implement: To include a doughnut chart to display to users the breakdown of cereals by manufacturer currently in the database.

6. User would like to have a quick overview of the detailed nutritional information of a particular cereals and manufacturer brand on the index page
Features to implement: To include a search form that uses AJAX query to retrieve the information from the database and display back to the user the cereals information they have queried for.

7. User would like to update or delete their ratings for a particular cereals
Features to implement: To include a user history page specific to that particular user that allows them to choose which ratings to be updated or removed.

8. User would like to update or delete the cereals nutritional information
Features to implement: To include a user history page specific to that particular user that allows them to choose which previous cereals contribution that they would like to update or delete.

## Project Structure
There are 3 main parts of this web application, i.e. user logging in / out, user registration and users accessing the web application features once they are logged in.

At the login page, existing user will need to login before they can access the in-app features of the web application. For new users, they will be redirected to the registration page to sign up for an account. 

Logged out features are only allowed for users which are currently logged in.

Once users are logged in, they will be redirect to the landing page, which comprise of the navbar at the uppermost of the web application. The navbar contains link to the search, contribute, history and logout page.

On the index page, users will be provided with an overview of the number of current records in the database, an overview of the cereal brands by manufacturer, a barchart comparing the top 3 cereals with the highest calories and an autocomplete search form that allows user to query for the nutritional information for a particular cereals.

On the search page, users will be able to search for a particular cereals based on one of the following options: manufacturer, cereals type, cereal name and calories. Results returned will be displayed in table format and when user clicks on the cereal name in the table they will be redirected to the ratings and reviews page.

On the history page, users will be able to view their own previous ratings or cereals contribution by clicking on either the ratings info or cereals info radiobutton. Upon clicking on either one of the selection, users will be redirected to the page whereby they will be allowed to edit or delete the ratings or contributions they have made previously.

Clicking on the logout button will logged the user out and clear the session related to that particluar user.

### b. Wireframes




### c. ER diagram
ER diagram was used for the database design. There are 5 tables that has been identified with this ER diagram. The 5 tables and their relationships between each other are as below:
Note:
- PK: primary key
- FK: foreign key

Tables: Cereals, Manufacturer, Type, Contribute, Users

Keys:
Cereals: cereal_id (PK), manufacturer_id (FK), type_id (FK)
Manufacturer: manufacturer_id (PK)
Type: type_id (PK)
Contribute: contribute_id (PK), user_id (FK), manufacturer_id (FK), cereal_id (FK)
Users: user_id (PK), name (FK), password (FK)

Entity Relationship (ER) diagram:

![ER diagram](https://www.lucidchart.com/publicSegments/view/7f769810-9a51-4ab5-b2c1-6051bbddc304/image.jpeg)


## Project Skeleton
### a. Existing Features
- Application was designed with Bootstrap grid design and mobile responsiveness in mind. 
- Users are able to login and logout of the web application.
- New user is able to sign up for a new account.
- Users are able to give reviews and ratings to their favourite cereals
- Users are able to update or delete their cereals ratings but not allowed to create duplicate ratings and reviews for a particular cereals
- Users are able to contribute new cereal nutritional information to the database.
- Users are able to update or delete their previous cereal contribution.
- Users are able to search for cereals information by selecting either the manufacturer, cereals type, cereal name or calories radiobuttons.
- Users are able to view their own previous ratings and cereal contributions.

### b. Features to be implemented in the future
For the future development of this cereal nutritional information web application, I would like to include features that will allow users to upload images of the cereal brands, brief description of the cereal brands and also features to allow user to follow and share their favourite cereals with each other.

## Project Surface





## Technologies used
1. HTML5 was the markup language used for structuring the content of the web application
2. CSS3 was a style sheet language used to format the outlook of the web application
3. JavaScript was the programming language to add front end interactivity to the web application
4. jQuery is a JavaScript library. It was used to manipulate the HTML DOM element, event handling, animation and AJAX - https://jquery.com/
5. Bootstrap 4 was the framework used to make the application responsive - https://getbootstrap.com/
6.  Github was used to deploy the web application    
7.  ChartJS was used to plot the barchart and doughnut chart found at the index page - https://www.chartjs.org/
8.  ChartJS plugins was used to display the labelling for the doughnut chart - https://github.com/emn178/chartjs-plugin-labels 
9.  Heroku ClearDB was used as the MySQL database to store all the datatables and datasets
10. HeidiSQL was used to view the structures and datasets in the database -  https://www.heidisql.com/
11. Github was used to deploy the web application
12. Twitter typeahead.js was used with the search form to incorporate the autocomplete function - https://github.com/twitter/typeahead.js
13. Python was used to write up the different routes to handle the different request method
14. Flask-MySQLdb was used to connect Flask with MySQL
15. LucidChart was used to tool up the ER diagram for the database design - https://www.lucidchart.com/

## Testing (Manual)
### Responsiveness
The web application was tested across multiple device screen sizes (small: iPhone 5, Galaxy S5, Pixel 2, medium: iPad, large: iPad Pro). Website scale responsively according to the device screen when tested in the Developer tools.

### Browser compatibility
The web application was tested and is compatible on Chrome, Opera and Firefox.

### Test Cases
| Test Case     | Description                   | Outcome  |
| ------------- |-----------------------------  | -------- |
|1              | New users will be redirected to the register page if they try to login with a username that does not exist. | Pass     |
|2              | New users can only register with a username that does not exist in the Users table in the database. If no record is found, user will be allowed
to register with the username that they have key in and a message will be popped up notifying the user that they have successfully registered for an account. | Pass     |
|3              | New users must provide a strong enough password during account resgistration, i.e. password must contain alphanumeric characters and special symbols(!@#$%^&*) and be 8 to 15 characters long. If password provided does not fulfill the password requirement criteria, an alert message will popped up to notify the user and the registration form will not be submitted to the backend to be persisted to the database. | Pass     |
|4              | Password and repeated password must be the same to register for a new user account. Else, an alert message will be popped up to notify the user that they have a mismatch password fields. | Pass     |
|5              | Upon logging in to the web application, users will reach the landing page whereby users will see a navbar on the top part of the website (which includes the contribute, search, history and logout tab). At the body section of the web application, users will be able to see a message at the top letting users know how many records are there currently in the database, a doughnut chart showing the breakdown of cereals by manufacturer, top 3 cereals with highest calories and an autocomplete search form that allows user to search for nutritional information of a particular cereals. | Pass     |
|6              | Upon clicking on the contribute tab of the navbar, users will be able to contribute new cereals information by filling up the form. If users select the "Others" option for the manufacturer category, users will need to provide a new name for the manufacturer. This new name will be checked against the Manufacturer table in the database. If it is found that the manufacturer name exist, the users will not be allowed to add that particular manufacturer to the database. All other fields must be provided, else the form will prompt the user to complete the fields before submitting the form to backend to be proceessed. | Pass     |
|7              | Upon clicking on the search tab of the navbar, users will be able to search for a particular cereals by manufacturer, cereals type, cereals name or calories. The results will be displayed in a table format based on the selection made. In the table, user will be able to see a summary of the cereals which includes the cereal name, manufacturer, cereal type and calories. If the user clicks on the cereal name, they will be redirected to the ratings page that allows them to give their reviews for that particular cereals. | Pass     |
|8              | Upon clicking on the history tab of the navbar, users will be brought to the history page that they need to choose either the ratings info or the cereals info radiobutton. When clicked on the ratings info radiobutton, user will be shown the previous ratings that they can edit or delete. When clicked on the cereal info radiobutton, user will be shown the previous cereals contribution they can update or delete. | Pass     |
|9              | If user choose to edit the previous ratings or cereal contribution, the edit form will be popped up with information that they have submitted previously from the database. | Pass     |
|10             | Messages will be flashed up everytime the users has successfully added, deleted or removed a record from the database. | Pass     |
|11             | Flashed messages is made to disappear after a certain time lapse using jQuery fadeOut function. | Pass     |
|12             | When user clicks on logout, they will logged out from the web application and the session related to the particular user will be cleared. | Pass     |
|13             | User will only be shown the ratings and contribution that they have made when they clicked on the history tab. This allows only the rightful owner to do the edit or delete of a record from the database. | Pass     |
|14             | Users are able to login if the correct username and password is provided. Else an error message of invalid username / password will be shown to the user. | Pass     |

## Bugs Discovered
No bugs found.

## Scripts to create datatables and import datasets to MySQL database
create_datatables.py - a Python script written to create all the tables needed in the MySQL database

import_datasets.py - a Python script written to automatically import all the datasets from the csv file to the MySQL database.

## How to use


## Deployment
### a. Heroku Deployment
1. Sign up for an account at [Heroku](https://www.heroku.com/).
2. Download Heroku CLI at [Heroku](https://devcenter.heroku.com/articles/heroku-cli#download-and-install) website.
3. Install the dowloaded Heroku CLI from Step 2
4. Open up Git Bash terminal. Cd to the location that you have your project in. Then, in the Git Bash Terminal, login to Heroku by typing ```heroku login```. A login page will be popped up to allow you to login to Heroku.
5. Open up another Git Bash terminal. Create a new app using ```heroku create <app_name>```.
6. In Git Bash, check whether the new remotes has been successfully added using ```git remote -v```.
7. In Git Bash, install gunicorn with the command ```git remote -v```.
8. Create a file called Procfile. Add ```web gunicorn app:app``` and save it.
9. Create the requirements.txt file with ```pip3 freeze --local > requirements.txt```.
10. In Git Bash, commit and push the project to Heroku with the following:
* ```git add .```
* ```git commit -m "<Commit Message>"```
* ```git push heroku master```
11. In Heroku, set up your key and value needed for the project. For this project, the database url, MySQL username and password has been configured.

### b. Setting up MySQL (ClearDB) with Heroku
1. Installing ClearDB in Git Bash using ```heroku addons:create cleardb:ignite```





### b. GitHub Deployment

session object
modal form edit 
