'''
    Citation for the following code:
    Course: CS340 - Introduction to Databases
    File: Routes for Venues CRUD implementation
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

from flask import Blueprint, render_template, jsonify, request
from .. import mysql

# Define blueprint for Venues
venues_bp = Blueprint(
    'venues_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

# Route to the frontend for managing Venues 
@venues_bp.route('/venues')   
def venues_home():
    return render_template('venues.j2')

"""
    CRUD FUNCTIONALITIES FOR VENUES
"""

# GET: Retrieve all venues names (for dropdown selection)
@venues_bp.route('/api/venues/names', methods=['GET'])
def get_venue_names():
    try:
        cursor = mysql.connection.cursor()
        # retreive only id, venue name data from all records in Venues
        query = 'SELECT venue_id, venue_name FROM Venues'  
        cursor.execute(query)
        venues = cursor.fetchall()
        cursor.close()

        print("✅ Retrieved venues:", venues)  # Debugging log
        return jsonify(venues), 200
    except Exception as e:
        print("❌ Error fetching venues:", str(e))
        return jsonify({'error': str(e)}), 500


# CREATE: Add a venue record
@venues_bp.route('/api/venues', methods=['POST'])
def add_venue():
    data = request.json

    # make sure that all required fields have been recieved to use in query
    if not data.get('venue_name') or not data.get('capacity') or 'is_wheelchair_accessible' not in data:
        return jsonify({'error': 'Missing required fields (venue_name, capacity, is_wheelchair_accessible)'}), 400

    try:
        cursor = mysql.connection.cursor()
        query = 'INSERT INTO Venues (venue_name, capacity, is_wheelchair_accessible) VALUES (%s, %s, %s)'
        # values recieved from the add venue form from frontend
        values = (data['venue_name'], int(data['capacity']), int(data['is_wheelchair_accessible']))
        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()
        
        return jsonify({'message': 'Venue added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# READ: Get all records within the Venues entity
@venues_bp.route('/api/venues', methods=['GET'])
def get_venues():
    try:
        cursor = mysql.connection.cursor()
        # retreive all attribute data from all records in Venues
        query = '''
            SELECT *
            FROM Venues
        '''
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

# UPDATE: Modify details of an existing venue record
@venues_bp.route('/api/venues/<int:venue_id>', methods=['PUT'])
def update_venue(venue_id):
    data = request.json
    print("🔹 Update Request Received for Venue ID:", venue_id, "| Data:", data)  # Debugging log

    # check that required attributes have been recieved from frontend to use in query
    if not data or not data.get('venue_name') or not data.get('capacity') or 'is_wheelchair_accessible' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        cursor = mysql.connection.cursor()
        # update specific venue record based on values recieved from edit form on frontend
        query = '''
            UPDATE Venues 
            SET venue_name = %s, capacity = %s, is_wheelchair_accessible = %s 
            WHERE venue_id = %s
        '''
        values = (data['venue_name'], int(data['capacity']), int(data['is_wheelchair_accessible']), venue_id)

        print("🔹 Executing query:", query) # debugging log
        print("🔹 With values:", values) # debugging log

        cursor.execute(query, values)
        if cursor.rowcount == 0:
            return jsonify({'error': 'No matching record found'}), 404

        mysql.connection.commit()
        cursor.close()
        
        return jsonify({'message': 'Venue updated successfully'}), 200
    except Exception as e:
        print("❌ SQL Error:", str(e))
        return jsonify({'error': str(e)}), 500


# DELETE: Remove a venue record
@venues_bp.route('/api/venues/<int:venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    try:
        cursor = mysql.connection.cursor()
        # delete the specified record and all attributes of that record
        query = 'DELETE FROM Venues WHERE venue_id = %s'
        # use venue_id recieved from delete form on frontend to find record to delete
        cursor.execute(query, (venue_id,))
        mysql.connection.commit()
        cursor.close()
        
        return jsonify({'message': 'Venue deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
