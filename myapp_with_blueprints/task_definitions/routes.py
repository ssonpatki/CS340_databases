'''
    Citation for the following code:
    Course: CS340 - Introduction to Databases
    File: Routes for Task_definitions CRUD implementation
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

# Define blueprint for Task_definitions
task_definitions_bp = Blueprint(
    'task_definitions_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

# Route to the frontend for managing Task_definitions 
@task_definitions_bp.route('/task_definitions')   
def task_definitions_home():
    return render_template('task_definitions.j2')

"""
    CRUD FUNCTIONALITIES FOR TASK_DEFINITIONS
"""

# CREATE: Add a new task definition record
@task_definitions_bp.route('/api/task_definitions', methods=['POST'])
def add_task_definition():
    data = request.json

    # make sure that all required fields have been recieved to use in query
    if not data.get('task_name') or not data.get('task_description') or not data.get('task_status'):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        cursor = mysql.connection.cursor()
        query = 'INSERT INTO Task_definitions (task_name, task_description, task_status) VALUES (%s, %s, %s)'
        # values recieved from the add task_definition form from frontend
        values = (data['task_name'], data['task_description'], data['task_status'])

        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()
        

        print("✅ Task Added:", values)  # Debugging log
        return jsonify({'message': 'Task definition added successfully'}), 201
    except Exception as e:
        print("❌ Error adding task:", str(e))
        return jsonify({'error': str(e)}), 500



# READ: Get all task definitions records
@task_definitions_bp.route('/api/task_definitions', methods=['GET'])
def get_task_definitions():
    try:
        cursor = mysql.connection.cursor()

        # retreive all attribute data from all records in task_definitions
        query = '''
            SELECT task_id, task_name, task_description, task_status 
            FROM Task_definitions
            ORDER BY task_name;
        '''
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# UPDATE: Modify details of an existing task definition record
@task_definitions_bp.route('/api/task_definitions/<int:task_id>', methods=['PUT'])
def update_task_definition(task_id):
    data = request.json

    # check that required attributes have been recieved from frontend to use in query
    if not data.get('task_name') or not data.get('task_description') or not data.get('task_status'):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        cursor = mysql.connection.cursor()
        # update specific task_definition record based on values recieved from edit form on frontend
        query = '''
            UPDATE Task_definitions 
            SET task_name = %s, task_description = %s, task_status = %s
            WHERE task_id = %s
        '''
        values = (data['task_name'], data['task_description'], data['task_status'], task_id)

        cursor.execute(query, values)
        if cursor.rowcount == 0:
            return jsonify({'error': 'No matching record found'}), 404

        mysql.connection.commit()
        cursor.close()
        
        return jsonify({'message': 'Task definition updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# DELETE: Remove a task definition record
@task_definitions_bp.route('/api/task_definitions/<int:task_id>', methods=['DELETE'])
def delete_task_definition(task_id):
    try:
        cursor = mysql.connection.cursor() 
        # delete the specified record and all attributes of that record
        query = 'DELETE FROM Task_definitions WHERE task_id = %s'
        # use task_id recieved from delete form on frontend to find record to delete
        cursor.execute(query, (task_id,))

        if cursor.rowcount == 0:
            return jsonify({'error': 'No matching record found'}), 404

        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Task definition deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
