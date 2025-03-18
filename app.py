'''
    Citation for the following code:
    Course: CS340 - Introduction to Databases
    File: Initiailizing app
    Database: SQL 
    Revised: 9 March 2025
    Sourced from: Flask Documentation 
    Source URL: 
        Flask Documentation Home Page: https://flask.palletsprojects.com/en/stable/
        Modular Applications with Blueprints: https://flask.palletsprojects.com/en/stable/blueprints/#my-first-blueprint
    Originality: Source code from article was used to learn how to implement an app with blueprints. 
    The following code is unique other than the general structure of the file. 
'''

from myapp_with_blueprints import create_app

app = create_app()

# Listener
if __name__ == "__main__":
    app.run(port=36190, debug=True)
