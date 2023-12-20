# Workout-Log
## Video Demo:  https://www.youtube.com/watch?v=4QFnmLeG88w
## ------ Description ------
### The Idea:
As someone who goes to the gym and tracks his workouts, I found it tedious to manually log my workout details using my phone's notepad. Realizing the need for efficiency, for my CS50 project, I embarked on creating an app that streamlines and refines the process of entering the number of reps and sets. This application is tailored to enhance the efficiency of tracking my workout days, ensuring a seamless and time-saving experience compared to the traditional note-taking method on my phone.
### About the Project:
Using Flask on Python, HTML and a bit of JS, I created a website/webapp for users to be able to enter their workout details. Intially, I had planned it to be able to be downloaded on phone and also be able to use it offline. Initially, I thought about instead of having a login/user based system, what if I instead stored the data locally on each users device using webSQL without needed to login, each person would have a unique instance with the data stored locally on their device. However, I soon abandoned the idea was it proved to be a bit too complicated for a beginner project. 

Then I thought about storing the data in the server but making the webapp downloadable and available offline using caching. For this task, I stumbled upon Progressive Webapps(PWA), Service-Workers and Workbox. After creating a demo, I tried to make it downloadable and work offline. Unfortunately, due to technicalites and complexities on how to make the Flask micro-framework compatibile with PWA's, this task turned to be way above my beginner-level pay-grade, hence it is an idea I want to revisit once I further develop my coding skills.
### Embarking on the Journey:
Starting the project, in order to refine my knowledge furthermore, I watched many different tutorials on Flask, Javascript and HTML. The first major problem I encountered was using a database with Flask. Turns out, the CS50 library made it really easy to use SQLite with Flask. However, without the CS50 library, I was left confused and overwhelmed on trying to use SQLite. Then, I found out about SQL-Alchemy on Flask, it took me a YouTube tutorial and a lot of googling for documentation to learn it, but I finally got the grasp of it. Following this, I learned Flask-Login for Authentication, Blueprints for routes in different files, a bit more of Javascript notation and how to make XML requests, and a whole lot of other stuff, it was a great journey of learning.
### How to use and file structure:
To run the program, run the main.py file and open the site. I did try to have the site hosted on heroku instead of relying locally hosting it, but it requried credit-details which I did not want to provide.
You may find the file structing interesting, the main.py file resides outside of where all the other dependencies reside. Indeed, all the routes and templates are to be found in the "webapp" folder, this folder contains the __init__.py file, which means it is intialized as a package. I stumbled upon this way of structuring after watching a tutorial on Flask on Youtube, it makes it really easy to import different functions from other python files.
#### Python Files:
main.py - Run this file to run the webpage, imports from the webapp directory the create_app function.
__init__.py - Defines the webapp directory as a package, also contains the create_app function which defines intializes the webapp, registers the blueprints, creates and intializes the database and the login manager.
auth.py - Contains the routes for login, register and logout, handles user authentication.
routes.py - Main routes file, handles all other routes for the webapp, handles insertion and deletion of rows in tables, most of the functionality of the webapp is based on the file.
table.py - Defines all the tables for SQL 
#### Templates:
Stored in the templates directory, contains all HTML for all the pages. All HTML files inherit from layout.html which contains the navbar, basic information about the page and defines JS and CSS routes.
#### Static:
Contains the CSS and JS files, you may also note it contains the manifest file and the logo of the webapp. The manifest file is used to give the app functionality to be able to be downloaded, currently it serves no useful purpose. The JS files contains functions to confirm certain actions. However, some JS scripts all the XML scripts are written within the HTML file themselves.
### Future plans:
I want to make this a proper downladable app in the future that will work offline. I want to make it more beautiful with the design too. I also want to improve the compare page by showing how many reps were less or more than the other week. 
