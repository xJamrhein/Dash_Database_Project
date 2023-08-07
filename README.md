# JeremyAmRhein

# Title: University Faculty Directory

# Purpose: 
The purpose of this application is to allow the user to explore the faculty members of various universities.  The target users are anyone who is interested in learning about and/or contacting a faculty member of a chosen university.  The application is also made for users who work for a university and would like to update the list of faculty at their university.

# Demo Link:
https://mediaspace.illinois.edu/media/t/1_gn2jb3ac

# Installation:
Only the given dataset was used for this application.  Installing the application requires the download of all of the python files in this repository.  One must run the neo4j database so that the application can query the neo4j database.  The mysql and mongodb databases do not need a running instance in order for the application to fully work.

# Usage:
The application is used by selecting a university at the top of the web page.  Selecting a university allows the below faculty table to populate as well as allow the other widgets in the application to filter their results.  The web page automatically starts by having the "University of illinois at Urbana Champaign" selected in the university dropdown.  After selecting a university, the user can look through the faculty table to find information about all of the faculty members at that university as well as see a count of how many faculty members exist at that university.  Below the faculty table on the left-hand side is a form that you can fill out.  This form allows the user to insert a faculty member and their information into the database.  After submitting the form and refreshing the webpage, you will be able to see in the faculty table the faculty member that was added from the form as long as you have selected the new faculty members affiliated university that you inserted it with.  To the right of the faculty insertion form is another dropdown where you can select any faculty member from the university that is selected.  After selecting a faculty member, the two widgets below the dropdown will populate.  These widgets show the user which keywords that the faculty is associated with and how many publications that that faculty member published.

# Design:
The design of the application uses various bordered rectangles to highlight a group of data as well as differentiate each section of the data from the rest of the webpage.  Each rectangle showcases static data that is achieved through using dropdowns to filter the data being shown.  There is also a form that the user can fill out in order to add to the data.  This form can only be submitted if all of the fields within the form are filled out.

# Implementation:
This application was implemented using the Dash python library.  All of the application was coded in python, and the functionality to interact with each of the 3 databases (mysql, mongodb, and neo4j) is coded in its own python file separate from the main python file that renders the web page.  I used visual studio code as my development environment as well as windows command prompt in order to run the application.  I also use neo4j desktop to run an instance of the neo4j database so that the neo4j queries will run successfully.  Most of the queries in the application use the mysql database.  The mongodb database is queried in order to return the various keywords associated with a chosen faculty member.  The neo4j database is queried in order to find the number of publications that a chosen faculty member published.  The items in each dropdown are from a mysql query, which are then passed to the respective mongodb and neo4j queries.

# Database techniques:
The 3 database techniques I used are
1. Indexing: I created an index in the mysql database on the name column of the faculty table to quickly retrieve the name values of all of the faculty members.  This was done as the faculty dropdown list needs to be populated quickly after selecting a university from the university dropdown.
2. View: I created a view in the mysql database which selects the count of the faculty members at a chosen university.  This view named "faculty count" selects the id of the selected university as well as the count of how many faculty members are affiliated with that university.  This view is queried and displayed with the faculty count widget at the top of the web page.
3. Prepared statements: I used a prepared statement for the faculty insertion form.  It is always good practice to use prepared sql statements, especially when dealing with user input, as it prevents the user from possibly altering the database with tactical input into the form.

# Contributions:
I worked on this project alone therefore I coded the entire application.

