'''
    Citation for the following code:
    Course: CS340 - Introduction to Databases
    File: Routes for Events CRUD implementation
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

# Define blueprint for events
events_bp = Blueprint(
    'events_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

# Route to the frontend for managing Events 
@events_bp.route('/events')  
def events_home():
    return render_template('events.j2')

"""
    CRUD FUNCTIONALITIES FOR EVENTS
"""

# GET: Retrieve all events names (for dropdown selection)
@events_bp.route('/api/events/names', methods=['GET'])
def get_events_names():
    try:
        cursor = mysql.connection.cursor()

        # retreive only id and event name data from all records in Events
        cursor.execute('SELECT event_id, event_name FROM Events')
        events = cursor.fetchall()
        cursor.close()
        
        return jsonify(events), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# CREATE: Add an event record
@events_bp.route('/api/events', methods=['POST'])
def add_event():
    data = request.json

    # make sure that all required fields have been recieved to use in query
    if not data.get('event_name') or not data.get('event_date') or 'total_attendees' not in data:
        return jsonify({'error': 'Missing required fields (event_name, event_date, total_attendees)'}), 400

    try:
        cursor = mysql.connection.cursor()
        query = '''
            INSERT INTO Events (event_name, event_date, total_attendees, venue_id)
            VALUES (%s, %s, %s, %s);

        '''
        # values recieved from the add event form from frontend
        values = (data['event_name'], data['event_date'], int(data['total_attendees']), int(data['venue_id']))
        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()
        
        return jsonify({'message': 'Venue added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# READ: Get all event records
@events_bp.route('/api/events', methods=['GET'])
def get_events():
    try:
        cursor = mysql.connection.cursor()

        # retreive all attribute data from all records in Events
        query = '''
            SELECT Events.event_id, Events.event_name, Events.event_date, Events.total_attendees, Venues.venue_name
            FROM Events
            INNER JOIN Venues ON Events.venue_id = Venues.venue_id;
        '''
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

# UPDATE: Modify details of an Event record
@events_bp.route('/api/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    data = request.json
    print("🔹 Update Request Received for Event ID:", event_id, "| Data:", data)  # Debugging log

    # check that required attributes have been recieved from frontend to use in query
    if not data or not data.get('event_name') or not data.get('event_date') or 'total_attendees' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        cursor = mysql.connection.cursor()
        query = '''
            UPDATE Events
            SET event_name = %s, event_date = %s, total_attendees = %s, venue_id = %s
            WHERE event_id = %s;

        '''
        # update specific event record based on values recieved from edit form on frontend
        values = (data['event_name'], data['event_date'], int(data['total_attendees']), int(data['venue_id']), event_id)

        print("🔹 Executing query:", query) # debugging log
        print("🔹 With values:", values)    # debugging log

        cursor.execute(query, values)
        if cursor.rowcount == 0:
            return jsonify({'error': 'No matching record found'}), 404

        mysql.connection.commit()
        cursor.close()
        
        return jsonify({'message': 'Event updated successfully'}), 200
    except Exception as e:
        print("❌ SQL Error:", str(e))
        return jsonify({'error': str(e)}), 500


# DELETE: Remove an event record
@events_bp.route('/api/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    try:
        cursor = mysql.connection.cursor()
        # delete the specified record and all attributes of that record
        query = 'DELETE FROM Events WHERE event_id = %s'
        # use event_id recieved from delete form on frontend to find record to delete
        cursor.execute(query, (event_id,))
        mysql.connection.commit()
        cursor.close()
        
        return jsonify({'message': 'Event deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
