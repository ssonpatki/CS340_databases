/*
    Citation for the following code:
    Course: CS340 - Introduction to Databases
    File: Data Definition Queries using Data Definition Language
    Database: SQL 
    Revised: 25 February 2025
    Sourced from: Oregon State Univerity Ecampus Course CS340 - Activity 1/2/3
    Source URL: 
        Activity 1: https://canvas.oregonstate.edu/courses/1987790/pages/activity-1-creating-a-customer-object-table?module_item_id=25022975
        Activity 3: https://canvas.oregonstate.edu/courses/1987790/pages/activity-3-creating-transaction-and-category-tables?module_item_id=25022977
    Originality: Source code used for inspiration to complete this assignment. Query structures are based on examples within the source code, but the specific 
    attributes and entities are specific to our unique db.
*/

SET FOREIGN_KEY_CHECKS = 0;
SET AUTOCOMMIT = 0;
    
/*
    Attendees Entity: records information about each individual attending the event, 
    including whether they are an employee/company representative, or simply attending the event 
*/

CREATE OR REPLACE TABLE Attendees (
    attendee_id int(11) NOT NULL AUTO_INCREMENT,
    first_name varchar(255) NOT NULL,
    last_name varchar(255) NOT NULL, 
    email varchar(255) NOT NULL,
    phone_number varchar(15) NOT NULL,
    is_employee tinyint(1) NOT NULL DEFAULT 0,
    PRIMARY KEY (attendee_id)
);

/*
   Venues Entity: records information about venue
*/

CREATE OR REPLACE TABLE Venues (
    venue_id int(11) NOT NULL AUTO_INCREMENT,    
    venue_name varchar(255) NOT NULL,
    capacity int(11) NOT NULL,
    is_wheelchair_accessible tinyint(1) NOT NULL DEFAULT 1,
    PRIMARY KEY (venue_id)
);

/*
    Events Entity: records basic information about an event 
*/

CREATE OR REPLACE TABLE Events (
    event_id int(11) NOT NULL AUTO_INCREMENT,   
    event_name varchar(255) NOT NULL UNIQUE,
    event_date date NOT NULL,
    total_attendees int(11) NOT NULL,
    venue_id int(11) NOT NULL,
    PRIMARY KEY (event_id),
    FOREIGN KEY(venue_id) REFERENCES Venues(venue_id) -- added specific reference for FK
);

/*
    Event_has_attendees: intersection table for Event and Attendees
*/

CREATE OR REPLACE TABLE Event_has_attendees (
    event_id int(11) NOT NULL,    -- not auto_increment because foreign key(?)
    attendee_id int(11) NOT NULL,
    FOREIGN KEY (event_id) REFERENCES Events(event_id) ON DELETE CASCADE ,     -- not sure if reference is necessary
    FOREIGN KEY (attendee_id) REFERENCES Attendees(attendee_id) ON DELETE CASCADE 
);


/*
    Task_definitions Entity: records information about tasks required to be completed 
    to ensure the event’s success
*/

CREATE OR REPLACE TABLE Task_definitions (
    task_id int(11) NOT NULL AUTO_INCREMENT,    -- added auto_increment
    task_name varchar(255) NOT NULL,
    task_description text NOT NULL,
    task_status varchar(255) NOT NULL,
    PRIMARY KEY (task_id)
);

/*
    Task_assignments Entity: creates an assignment ID for a task, as well as 
        1) the ID of the original task details (from the Task_definitions entity), 
        2) the event its associated with (found in the Events entity), 
    and 3) the ID of the attendee that should complete the task 

*/

CREATE OR REPLACE TABLE Task_assignments (
    assignment_id int(11) NOT NULL AUTO_INCREMENT,
    task_id int(11) NOT NULL,
    event_id int(11) NOT NULL,
    attendee_id int(11),    -- optional, in case task has not been assigned (yet) to a specific individual
    PRIMARY KEY (assignment_id),
    FOREIGN KEY (task_id) REFERENCES Task_definitions(task_id) ON DELETE CASCADE,
    FOREIGN KEY(event_id) REFERENCES Events(event_id) ON DELETE CASCADE,
    FOREIGN KEY(attendee_id) REFERENCES Attendees(attendee_id)  ON DELETE CASCADE -- added specific reference for FK
);


/*
    Queries to insert sample data 
    Note: (SELECT <attribute_name> FROM <table_name> WHERE <attribute_name> ='') is used 
    when value of a FK attribute is unknown
*/

-- populate Attendees table

INSERT INTO Attendees (first_name, last_name, email, phone_number, is_employee)
VALUES ('John', 'Doe', 'john.doe@email.com',	'555-111-1111', 1),    -- is_employee = 0 means not an employee
('Alice', 'Smith', 'alice.smith@email.com', '555-222-2222', 1),
('Bob', 'Johnson', 'bob.johnson@email.com', '555-333-3333', 0),
('Emma', 'Brown', 'emma.brown@email.com', '555-444-4444', 1),
('Liam', 'Wilson', 'liam.wilson@email.com', '555-555-5555', 0);
-- populate Venues table

INSERT INTO Venues (venue_name, capacity, is_wheelchair_accessible)    
VALUES ('Grand Hall', 500, 1),    -- is_wheelchair_accessible = 0 means not accessible
('Conference Room A', 100, 1),
('Outdoor Pavilion', 300, 0),
('City Auditorium', 600, 1),
('Skyline Banquet Hall', 250, 1);

-- populate Events table 

INSERT INTO Events (event_name, event_date, total_attendees, venue_id)
VALUES ('Tech Summit 2025', '2025-03-15', 200, (SELECT venue_id FROM Venues WHERE venue_id = 1)),
('Annual Gala Dinner',	'2025-06-10', 150, (SELECT venue_id FROM Venues WHERE venue_id = 2)),
('AI Research Symposium', '2025-09-25', 250, (SELECT venue_id FROM Venues WHERE venue_id = 3)),
('Robotics Expo 2025', '2025-04-20', 300, (SELECT venue_id FROM Venues WHERE venue_id = 4)),
('Healthcare Innovation Forum', '2025-05-05', 180, (SELECT venue_id FROM Venues WHERE venue_id = 5)); -- does not require SELECT unless value of FK is unknown


-- populate Event_has_attendees intersection table

INSERT INTO Event_has_attendees (event_id, attendee_id)
VALUES ((SELECT event_id FROM Events WHERE event_id = 1), (SELECT attendee_id FROM Attendees WHERE attendee_id = 1)),
((SELECT event_id FROM Events WHERE event_id = 1), (SELECT attendee_id FROM Attendees WHERE attendee_id = 3)),
((SELECT event_id FROM Events WHERE event_id = 2), (SELECT attendee_id FROM Attendees WHERE attendee_id = 2)),
((SELECT event_id FROM Events WHERE event_id = 2), (SELECT attendee_id FROM Attendees WHERE attendee_id = 4)),
((SELECT event_id FROM Events WHERE event_id = 3), (SELECT attendee_id FROM Attendees WHERE attendee_id = 5));

-- populate Task_definitions table

INSERT INTO Task_definitions (task_name, task_description, task_status)
VALUES ('Check in with caterers', 'Confirm catering services for event', 'Pending'),
('Set up registration desk', 'Arrange materials and check-in lists', 'Completed'),
('Keynote Speech Preparation', 'Ensure keynote speaker has necessary setup', 'In Progress'),
('Tech Equipment Setup', 'Set up microphones, projectors, and laptops', 'Completed'),
('Arrange Seating Plan', 'Organize seating for attendees', 'Pending');


-- populate Task_assignments table

INSERT INTO Task_assignments (task_id, event_id, attendee_id)
VALUES ((SELECT task_id FROM Task_definitions WHERE task_id = 1), (SELECT event_id FROM Events WHERE event_id = 1), (SELECT attendee_id FROM Attendees WHERE attendee_id = 1)),
((SELECT task_id FROM Task_definitions WHERE task_id = 2), (SELECT event_id FROM Events WHERE event_id = 1), (SELECT attendee_id FROM Attendees WHERE attendee_id = 2)),
((SELECT task_id FROM Task_definitions WHERE task_id = 3), (SELECT event_id FROM Events WHERE event_id = 2), (SELECT attendee_id FROM Attendees WHERE attendee_id = 3)),
((SELECT task_id FROM Task_definitions WHERE task_id = 1), (SELECT event_id FROM Events WHERE event_id = 3), (SELECT attendee_id FROM Attendees WHERE attendee_id = 1)),
((SELECT task_id FROM Task_definitions WHERE task_id = 2), (SELECT event_id FROM Events WHERE event_id = 3), (SELECT attendee_id FROM Attendees WHERE attendee_id = 2));
