'''
    Citation for the following code:
    Course: CS340 - Introduction to Databases
    File: Routes for Task_assignments CRUD implementation
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

from flask import Blueprint, render_template, request, jsonify
from .. import mysql

# Define blueprint for Task_assignments
task_assignments_bp = Blueprint(
    'task_assignments_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

# Route to the frontend for managing Task_assignments 
@task_assignments_bp.route('/task_assignments')   
def task_assignments_home():
    return render_template('task_assignments.j2')

"""
    CRUD FUNCTIONALITIES FOR TASK_ASSIGNMENTS
"""

# GET: Retrieve all tasks (for dropdown selection)
@task_assignments_bp.route('/api/tasks', methods=['GET'])
def get_tasks():
    try:
        cursor = mysql.connection.cursor()

        # retreive only id, task_name data from all records in Task_definitions
        query = 'SELECT task_id, task_name FROM Task_definitions'  # Use task_definitions instead of tasks
        cursor.execute(query)
        tasks = cursor.fetchall()
        cursor.close()
        

        print("✅ Retrieved tasks:", tasks)  # Debugging log
        return jsonify(tasks), 200
    except Exception as e:
        print("❌ Error fetching tasks:", str(e))
        return jsonify({'error': str(e)}), 500


# CREATE: Add a new task assignment record
@task_assignments_bp.route('/api/task_assignments', methods=['POST'])
def add_task_assignment():
    data = request.json
    print("🔹 Received Task Assignment Data:", data)  # Debugging log

    # make sure that all required fields have been recieved to use in query
    if not data.get('task_id') or not data.get('event_id') or not data.get('attendee_id'):
        print("❌ Missing required fields:", data)  # Debugging log
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        cursor = mysql.connection.cursor()

        query = '''
            INSERT INTO Task_assignments (task_id, event_id, attendee_id) 
            VALUES (%s, %s, %s)
        '''
        # values recieved from the add task form from frontend
        values = (data['task_id'], data['event_id'], data['attendee_id'])

        print("🔹 Executing Query:", query)  # Debugging log
        print("🔹 With Values:", values)  # Debugging log

        cursor.execute(query, values)
        mysql.connection.commit()

        print("✅ Task assignment added successfully!")  # Debugging log

        cursor.close()
        
        return jsonify({'message': 'Task assignment added successfully'}), 201
    except Exception as e:
        print("❌ SQL Error:", str(e))  # Debugging log
        return jsonify({'error': str(e)}), 500


# READ: Get all task assignments records with task, event, and assignee names
@task_assignments_bp.route('/api/task_assignments', methods=['GET'])
def get_task_assignments():
    try:
        cursor = mysql.connection.cursor()

        # retreive all attribute data from all records in Tasks
        # necessary to use Join because of FKs attributes in the record
        query = '''
            SELECT Task_assignments.assignment_id, 
                Task_definitions.task_name, 
                Events.event_name, 
                CONCAT(Attendees.first_name, ' ', Attendees.last_name) AS attendee_name
            FROM Task_assignments
            INNER JOIN Task_definitions ON Task_assignments.task_id = Task_definitions.task_id
            INNER JOIN Events ON Task_assignments.event_id = Events.event_id
            LEFT JOIN Attendees ON Task_assignments.attendee_id = Attendees.attendee_id
        '''

        cursor.execute(query)
        task_assignments = cursor.fetchall()
        cursor.close()

    
        print("🔹 Task Assignments Fetched:", task_assignments)  # Debugging log
        return jsonify(task_assignments), 200
    except Exception as e:
        print("❌ Error fetching task assignments:", str(e))  # Debugging log
        return jsonify({'error': str(e)}), 500


# UPDATE: Modify an existing task assignment record
@task_assignments_bp.route('/api/task_assignments/<int:assignment_id>', methods=['PUT'])
def update_task_assignment(assignment_id):
    data = request.json
    print("🔹 Received Task Assignment Update Data:", data)  # Debugging log

    # Ensure all required fields are present and properly typed
    if not data.get('task_id') or not data.get('event_id') or not data.get('attendee_id'):
        print("❌ Missing required fields:", data)  # Debugging log
        return jsonify({'error': 'Missing required fields'}), 400

    # Cast values to integers to ensure they're in the correct format
    try:
        task_id = int(data['task_id'])
        event_id = int(data['event_id'])
        attendee_id = int(data['attendee_id'])
    except ValueError:
        return jsonify({'error': 'task_id, event_id, and attendee_id must be integers'}), 400

    try:
        cursor = mysql.connection.cursor()

        # Log the query being executed and the values
        query = '''
            UPDATE Task_assignments 
            SET task_id = %s, event_id = %s, attendee_id = %s
            WHERE assignment_id = %s
        '''
        values = (task_id, event_id, attendee_id, assignment_id)

        print("🔹 Executing Query:", query)  # Debugging log
        print("🔹 With Values:", values)  # Debugging log

        cursor.execute(query, values)

        # Check if a record was updated
        if cursor.rowcount == 0:
            print("❌ No matching record found for update.")  # Debugging log
            return jsonify({'error': 'No matching record found'}), 404

        mysql.connection.commit()

        print("✅ Task assignment updated successfully!")  # Debugging log

        cursor.close()
        
        return jsonify({'message': 'Task assignment updated successfully'}), 200
    except Exception as e:
        print("❌ SQL Error:", str(e))  # Debugging log
        return jsonify({'error': str(e)}), 500


# DELETE: Remove a task assignment record
@task_assignments_bp.route('/api/task_assignments/<int:assignment_id>', methods=['DELETE'])
def delete_task_assignment(assignment_id):
    try:
        cursor = mysql.connection.cursor()
        # delete the specified record and all attributes of that record
        query = 'DELETE FROM Task_assignments WHERE assignment_id = %s'
        # use assignment_id recieved from delete form on frontend to find record to delete
        cursor.execute(query, (assignment_id,))

        if cursor.rowcount == 0:
            return jsonify({'error': 'No matching record found'}), 404

        mysql.connection.commit()
        cursor.close()
        
        return jsonify({'message': 'Task assignment deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

