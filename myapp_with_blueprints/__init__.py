'''
    Citation for the following code:
    Course: CS340 - Introduction to Databases
    File: Registering Blueprints
    Database: SQL 
    Revised: 9 March 2025
    Sourced from: Flask Documentation 
    Source URL: 
        Flask Documentation Home Page: https://flask.palletsprojects.com/en/stable/
        Modular Applications with Blueprints: https://flask.palletsprojects.com/en/stable/blueprints/#my-first-blueprint
    Originality: Source code from article was used to learn how to implement blueprints. 
    The following code is unique other than the general structure of the file. 
'''

from flask import Flask
from flask_mysqldb import MySQL

mysql = MySQL()

def create_app():
    app = Flask(__name__)

    # connect to mySQL database
    app.config["MYSQL_HOST"] = "classmysql.engr.oregonstate.edu"
    app.config["MYSQL_USER"] = "cs340_sonpatks"
    app.config["MYSQL_PASSWORD"] = "8739"
    app.config["MYSQL_DB"] = "cs340_sonpatks"
    app.config["MYSQL_CURSORCLASS"] = "DictCursor"

    mysql.init_app(app)
    
    # Import blueprints for index page and manage entities pages
    from .home.routes import home_bp
    from .attendees.routes import attendees_bp
    from .event_has_attendees.routes import event_has_attendees_bp
    from .events.routes import events_bp
    from .task_assignments.routes import task_assignments_bp
    from .task_definitions.routes import task_definitions_bp
    from .venues.routes import venues_bp


    # Register blueprints
    app.register_blueprint(home_bp, url_prefix='/')  # Main index page
    app.register_blueprint(attendees_bp, url_prefix='/attendees')
    app.register_blueprint(event_has_attendees_bp, url_prefix='/event_has_attendees')
    app.register_blueprint(events_bp, url_prefix='/events')
    app.register_blueprint(task_assignments_bp, url_prefix='/task_assignments')
    app.register_blueprint(task_definitions_bp, url_prefix='/task_definitions')
    app.register_blueprint(venues_bp, url_prefix='/venues')

    return app
