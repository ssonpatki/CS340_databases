from flask import Flask, render_template, json, redirect, jsonify
from flask_mysqldb import MySQL
from flask import request
import os


app = Flask(__name__)

app.config["MYSQL_HOST"] = "classmysql.engr.oregonstate.edu"
app.config["MYSQL_USER"] = "cs340_[username]"
app.config["MYSQL_PASSWORD"] = "[password]"
app.config["MYSQL_DB"] = "cs340_[username]"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

# Routes
# route homepage to /index by default 
@app.route("/")
def home():
    return redirect("/index")

# route for index page

@app.route("/index")
def index():
    return render_template("index.j2")

# route for attendees page
@app.route("/attendees")
def attendees():
    return render_template("attendees.j2")  

# route for events page
@app.route("/events")
def events():
    return render_template("events.j2")  

# route for event_has_attendees page
@app.route("/event_has_attendees")
def event_has_attendees():
    return render_template("event_has_attendees.j2")  

# route for task_assignments page
@app.route("/task_assignments")
def task_assignments():
    return render_template("task_assignments.j2")  

# route for task_definitions page
@app.route("/task_definitions")
def task_definitions():
    return render_template("task_definitions.j2")

# route for venues page
@app.route("/venues")
def venues():
    return render_template("venues.j2")  


# CREATE: Add an attendee to an event
@app.route('/api/event_has_attendees', methods=['POST'])
def add_event_attendee():
    data = request.json
    if not data.get('event_id') or not data.get('attendee_id'):
        return jsonify({'error': 'Missing event_id or attendee_id'}), 400

    try:
        cursor = mysql.connection.cursor()
        check_query = '''
            SELECT 1 FROM Event_has_attendees
            WHERE event_id = %s AND attendee_id = %s
        '''
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
        mysql.connection.rollback()
        return jsonify({'error': str(e)}), 500

# READ: View all event-attendee pairs
@app.route('/api/event_has_attendees', methods=['GET'])
def get_event_attendees():
    try:
        cursor = mysql.connection.cursor()
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

# UPDATE: Change the attendee for a specific event
@app.route('/api/event_has_attendees', methods=['PUT'])
def update_event_attendee():
    data = request.json
    if not all(k in data for k in ('event_id', 'attendee_id', 'new_event_id', 'new_attendee_id')):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        cursor = mysql.connection.cursor()
        query = '''
            UPDATE Event_has_attendees
            SET event_id = %s, attendee_id = %s
            WHERE event_id = %s AND attendee_id = %s
        '''
        cursor.execute(query, (data['new_event_id'], data['new_attendee_id'], data['event_id'], data['attendee_id']))
        if cursor.rowcount == 0:
            return jsonify({'error': 'No matching record found'}), 404

        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Event attendee updated successfully'}), 200
    except Exception as e:
        mysql.connection.rollback()
        return jsonify({'error': str(e)}), 500

# DELETE: Remove an attendee from an event
@app.route('/api/event_has_attendees', methods=['DELETE'])
def delete_event_attendee():
    data = request.json
    if not data.get('event_id') or not data.get('attendee_id'):
        return jsonify({'error': 'Missing event_id or attendee_id'}), 400

    try:
        cursor = mysql.connection.cursor()
        query = 'DELETE FROM Event_has_attendees WHERE event_id = %s AND attendee_id = %s'
        cursor.execute(query, (data['event_id'], data['attendee_id']))
        if cursor.rowcount == 0:
            return jsonify({'error': 'No matching record found'}), 404

        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Attendee removed from event successfully'}), 200
    except Exception as e:
        mysql.connection.rollback()
        return jsonify({'error': str(e)}), 500


# Listener
# change the port number if deploying on the flip servers
if __name__ == "__main__":
    app.run(port=36180, debug=True)