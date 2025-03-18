'''
    Citation for the following code:
    Course: CS340 - Introduction to Databases
    File: Routes for Attendees CRUD implementation
    Database: SQL 
    Revised: 9 March 2025
    Sourced from: Oregon State Univerity Ecampus Course CS340 - Exploration - Developing in Flask
    Source URL: 
        Exploration: https://canvas.oregonstate.edu/courses/1987790/pages/exploration-developing-in-flask?module_item_id=25023028 
        Flask Starter App: https://github.com/osu-cs340-ecampus/flask-starter-app 
        app.py file from bsg_people: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py 
    Originality: Source code from app.py was used to start this assignment, and learn how to utilize routes and implement CRUD functionalities. 
    The following code is unique other than database connection code and the general structure of the functions. 
'''

from flask import Blueprint, render_template, jsonify, request
from .. import mysql

# Define blueprint for attendees
attendees_bp = Blueprint(
    'attendees_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

# Route to the frontend for managing Attendees  
@attendees_bp.route('/attendees')  
def attendees_home():
    return render_template('attendees.j2')


"""
    CRUD FUNCTIONALITIES FOR ATTENDEES
"""

# GET: Retrieve all attendees names (for dropdown selection)
@attendees_bp.route('/api/attendees/names', methods=['GET'])
def get_attendees_names():
    try:
        cursor = mysql.connection.cursor()

        # retreive only id, first, and last name data from all records in Attendees
        query = '''
            SELECT attendee_id, first_name, last_name 
            FROM Attendees
        '''
        cursor.execute(query)
        attendees = cursor.fetchall()
        cursor.close()
        
        return jsonify(attendees), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# CREATE: Add an attendee record
@attendees_bp.route('/api/attendees', methods=['POST'])
def add_attendee():
    data = request.json

    # make sure that all required fields have been recieved to use in query
    if not data or not data.get('first_name') or 'last_name' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        cursor = mysql.connection.cursor()
        query = '''
            INSERT INTO Attendees (first_name, last_name, email, phone_number, is_employee)
            VALUES (%s, %s, %s, %s, %s);
        '''
        # values recieved from the add attendee form from frontend
        values = (data['first_name'], data['last_name'], data['email'], data['phone_number'], int(data['is_employee']))

        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()
        
        return jsonify({'message': 'Attendee added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# READ: Get all attendee records
@attendees_bp.route('/api/attendees', methods=['GET'])
def get_attendees():
    try:
        cursor = mysql.connection.cursor()

        # retreive all attribute data from all records in Attendees
        query = '''
            SELECT *
            FROM Attendees
        '''
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# UPDATE: Modify details of an attendee record
@attendees_bp.route('/api/attendees/<int:attendee_id>', methods=['PUT'])
def update_attendee(attendee_id):
    data = request.json
    print("🔹 Update Request Received for Attendee ID:", attendee_id, "| Data:", data)  # Debugging log

    # check that required attributes have been recieved from frontend to use in query
    if not data or not data.get('first_name') or 'last_name' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        cursor = mysql.connection.cursor()

        # update specific attendee record based on values recieved from edit form on frontend
        query = '''
            UPDATE Attendees
            SET first_name =  %s, last_name =  %s, email =  %s, phone_number =  %s, is_employee =  %s
            WHERE attendee_id = %s;
        '''
        values = (data['first_name'], data['last_name'], data['email'], data['phone_number'], int(data['is_employee']), attendee_id)

        print("🔹 Executing query:", query)
        print("🔹 With values:", values)

        cursor.execute(query, values)
        if cursor.rowcount == 0:
            return jsonify({'error': 'No matching record found'}), 404

        mysql.connection.commit()
        cursor.close()
        
        return jsonify({'message': 'Attendee updated successfully'}), 200
    except Exception as e:
        print("❌ SQL Error:", str(e))
        return jsonify({'error': str(e)}), 500


# DELETE: Remove an attendee record from entity
@attendees_bp.route('/api/attendees/<int:attendee_id>', methods=['DELETE'])
def delete_attendee(attendee_id):
    try:
        cursor = mysql.connection.cursor()
        # delete the specified record and all attributes of that record
        query = '''
            DELETE FROM Attendees 
            WHERE attendee_id = %s
        '''
        # use attendee_id recieved from delete form on frontend to find record to delete
        cursor.execute(query, (attendee_id,))
        mysql.connection.commit()
        cursor.close()
        
        return jsonify({'message': 'Attendee deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

