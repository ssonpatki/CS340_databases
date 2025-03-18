'''
    Citation for the following code:
    Course: CS340 - Introduction to Databases
    File: Routes for Events_has_attendees CRUD implementation
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


# Define blueprint for Event_has_attendees
event_has_attendees_bp = Blueprint(
    'event_has_attendees_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

# Route to the frontend for managing Event_has_attendees  
@event_has_attendees_bp.route('/event_has_attendees')  
def event_has_attendees_home():
    return render_template('event_has_attendees.j2')

"""
    CRUD FUNCTIONALITIES FOR EVENT_HAS_ATTENDEES
"""

# CREATE: Add an attendee to an event (i.e., add record of an individual attending a specific event)
@event_has_attendees_bp.route('/api/event_has_attendees', methods=['POST'])
def add_event_attendee():
    data = request.json

    # make sure that all required fields have been recieved to use in query
    if not data.get('event_id') or not data.get('attendee_id'):
        return jsonify({'error': 'Missing event_id or attendee_id'}), 400

    try:
        cursor = mysql.connection.cursor()
        check_query = '''
            SELECT 1 FROM Event_has_attendees
            WHERE event_id = %s AND attendee_id = %s
        '''
        # values recieved from the add attendee to event form from frontend
        cursor.execute(check_query, (data['event_id'], data['attendee_id']))
        existing_entry = cursor.fetchone()

        if existing_entry:
            return jsonify({'error': 'Attendee is already added to the event'}), 400

        insert_query = 'INSERT INTO Event_has_attendees (event_id, attendee_id) VALUES (%s, %s)'
        cursor.execute(insert_query, (data['event_id'], data['attendee_id']))
        mysql.connection.commit()
        cursor.close()
        

        return jsonify({'message': 'Attendee added to event successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# READ: View all event-attendee pairs
@event_has_attendees_bp.route('/api/event_has_attendees', methods=['GET'])
def get_event_attendees():
    try:
        cursor = mysql.connection.cursor()
        # retreive all records in Event_has_attendees 
        # need to use Join because of FK attributes from Events and Attendees
        query = '''
            SELECT eha.event_id, e.event_name, e.event_date, a.attendee_id, a.first_name, a.last_name
            FROM Event_has_attendees AS eha
            JOIN Events AS e ON eha.event_id = e.event_id
            JOIN Attendees AS a ON eha.attendee_id = a.attendee_id
        '''
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# UPDATE: Change the attendee and/or event information for a specific attendee-event pair
@event_has_attendees_bp.route('/api/event_has_attendees', methods=['PUT'])
def update_event_attendee():
    data = request.json

    # check that required attributes have been recieved from frontend to use in query
    if not all(k in data for k in ('event_id', 'attendee_id', 'new_event_id', 'new_attendee_id')):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        cursor = mysql.connection.cursor()
        # update specific event attendee record based on values recieved from edit form on frontend 
        # event and attendee have nullable relationship because an attendee may not be attending an event
        query = '''
            UPDATE Event_has_attendees
            SET event_id = %s, attendee_id = %s
            WHERE event_id = %s AND attendee_id = %s
        '''
        cursor.execute(query, (data['new_event_id'], data['new_attendee_id'], data['event_id'], data['attendee_id']))
        mysql.connection.commit()
        cursor.close()
        
        return jsonify({'message': 'Event attendee updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# DELETE: Remove an attendee from an event
@event_has_attendees_bp.route('/api/event_has_attendees', methods=['DELETE'])
def delete_event_attendee():
    data = request.json

    if not data.get('event_id') or not data.get('attendee_id'):
        return jsonify({'error': 'Missing event_id or attendee_id'}), 400

    try:
        cursor = mysql.connection.cursor()
        # delete the specified record and all attributes of that record
        query = 'DELETE FROM Event_has_attendees WHERE event_id = %s AND attendee_id = %s'
        # use data recieved from delete form on frontend to find record to delete
        cursor.execute(query, (data['event_id'], data['attendee_id']))
        mysql.connection.commit()
        cursor.close()
        
        return jsonify({'message': 'Attendee removed from event successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


