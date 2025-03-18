'''
    Citation for the following code:
    Course: CS340 - Introduction to Databases
    File: Routes for Home Page
    Database: SQL 
    Revised: 9 March 2025
    Sourced from: Oregon State Univerity Ecampus Course CS340 - Exploration - Developing in Flask
    Source URL: 
        Exploration: https://canvas.oregonstate.edu/courses/1987790/pages/exploration-developing-in-flask?module_item_id=25023028 
        Flask Starter App: https://github.com/osu-cs340-ecampus/flask-starter-app 
        app.py file from bsg_people: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py 
    Originality: Source code from app.py was used to start this assignment, and learn how to utilize routes and implement CRUD functionalities. 
    The following code is unique other than database connection code and the general structure of the file. 
'''

from flask import Blueprint, render_template, redirect
from .. import mysql

# Define blueprint for index page
home_bp = Blueprint(
    'home_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

# Routes

# Route to frontend index page of UI
@home_bp.route("/")
def index():
    return render_template('index.j2')