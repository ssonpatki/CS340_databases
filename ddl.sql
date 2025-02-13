/*
    Course: CS340 - Introduction to Databases
    Assignment: Project Step 2 Draft - Normalized Schema + DDL with Sample Data 
    File: Data Definition Queries using Data Definition Language
    Database: SQL  
    Due Date: 6 February 2025
*/

SET FOREIGN_KEY_CHECKS = 0;
SET AUTOCOMMIT = 0;
    
/*
    Queries to create the tables 
*/

-- Had to change the order of entities in order for the tables to populate without errors

CREATE OR REPLACE TABLE Attendees (
    attendee_id int(11) NOT NULL AUTO_INCREMENT,
    first_name varchar(255) NOT NULL,
    last_name varchar(255) NOT NULL, 
    email varchar(255) NOT NULL UNIQUE,
    phone_number varchar(255) NOT NULL UNIQUE,
    is_employee tinyint(1) NOT NULL DEFAULT 0,
    PRIMARY KEY (attendee_id)
);

CREATE OR REPLACE TABLE Venues (
    venue_id int(11) NOT NULL AUTO_INCREMENT,    
    venue_name varchar(255) NOT NULL,
    capacity int(11) NOT NULL,
    is_wheelchair_accessible tinyint(1) NOT NULL DEFAULT 1,
    PRIMARY KEY (venue_id)
);

CREATE OR REPLACE TABLE Events (
    event_id int(11) NOT NULL AUTO_INCREMENT,   
    event_name varchar(255) NOT NULL UNIQUE,
    event_date date NOT NULL,
    total_attendees int(11) NOT NULL,
    venue_id int(11) NOT NULL,
    PRIMARY KEY (event_id),
    FOREIGN KEY(venue_id) REFERENCES Venues(venue_id) -- added specific reference for FK
);

CREATE OR REPLACE TABLE Event_has_attendees (
    event_id int(11) NOT NULL,    -- not auto_increment because foreign key(?)
    attendee_id int(11) NOT NULL,
    FOREIGN KEY (event_id) REFERENCES Events(event_id) ON DELETE CASCADE ,     -- not sure if reference is necessary
    FOREIGN KEY (attendee_id) REFERENCES Attendees(attendee_id) ON DELETE CASCADE 
);

CREATE OR REPLACE TABLE Task_definitions (
    task_id int(11) NOT NULL AUTO_INCREMENT,    -- added auto_increment
    task_name varchar(255) NOT NULL,
    task_description text NOT NULL,
    task_status varchar(255) NOT NULL,
    PRIMARY KEY (task_id)
);

CREATE OR REPLACE TABLE Task_assignments (
    assignment_id int(11) NOT NULL AUTO_INCREMENT,
    task_id int(11) NOT NULL,
    event_id int(11) NOT NULL,
    attendee_id int(11),
    PRIMARY KEY (assignment_id),
    FOREIGN KEY (task_id) REFERENCES Task_definitions(task_id),
    FOREIGN KEY(event_id) REFERENCES Events(event_id),
    FOREIGN KEY(attendee_id) REFERENCES Attendees(attendee_id)  -- added specific reference for FK
);


/*
    Queries to insert sample data 
    Note: (SELECT <attribute_name> FROM <table_name> WHERE <attribute_name> ='') is used 
    when value of a FK attribute is unknown
*/

-- populate Attendees table

INSERT INTO Attendees (attendee_id, first_name, last_name, email, phone_number, is_employee)
VALUES (1, 'John', 'Doe', 'john.doe@email.com',	'555-111-1111', 1),    -- is_employee = 0 means not an employee
(2, 'Alice', 'Smith', 'alice.smith@email.com', '555-222-2222', 1),
(3, 'Bob', 'Johnson', 'bob.johnson@email.com', '555-333-3333', 0),
(4, 'Emma', 'Brown', 'emma.brown@email.com', '555-444-4444', 1),
(5, 'Liam', 'Wilson', 'liam.wilson@email.com', '555-555-5555', 0);

-- populate Events table 

INSERT INTO Events (event_id, event_name, event_date, total_attendees, venue_id)
VALUES (1, 'Tech Summit 2025', '2025-3-15', 200, (SELECT venue_id FROM Venues WHERE venue_id = 1)),
(2, 'Annual Gala Dinner',	'2025-6-10', 150, (SELECT venue_id FROM Venues WHERE venue_id = 2)),
(3, 'AI Research Symposium', '2025-9-25', 250, (SELECT venue_id FROM Venues WHERE venue_id = 3)),
(4, 'Robotics Expo 2025', '2025-4-20', 300, (SELECT venue_id FROM Venues WHERE venue_id = 4)),
(5, 'Healthcare Innovation Forum', '2025-5-5', 180, (SELECT venue_id FROM Venues WHERE venue_id = 5)); -- does not require SELECT unless value of FK is unknown

-- populate Venues table

INSERT INTO Venues (venue_id, venue_name, capacity, is_wheelchair_accessible)    
VALUES (1, 'Grand Hall', 500, 1),    -- is_wheelchair_accessible = 0 means not accessible
(2, 'Conference Room A', 100, 1),
(3, 'Outdoor Pavilion', 300, 0),
(4, 'City Auditorium', 600, 1),
(5, 'Skyline Banquet Hall', 250, 1);

-- populate Event_has_attendees intersection table

INSERT INTO Event_has_attendees (event_id, attendee_id)
VALUES ((SELECT event_id FROM Events WHERE event_id = 1), (SELECT attendee_id FROM Attendees WHERE attendee_id = 1)),
((SELECT event_id FROM Events WHERE event_id = 1), (SELECT attendee_id FROM Attendees WHERE attendee_id = 3)),
((SELECT event_id FROM Events WHERE event_id = 2), (SELECT attendee_id FROM Attendees WHERE attendee_id = 2)),
((SELECT event_id FROM Events WHERE event_id = 2), (SELECT attendee_id FROM Attendees WHERE attendee_id = 4)),
((SELECT event_id FROM Events WHERE event_id = 3), (SELECT attendee_id FROM Attendees WHERE attendee_id = 5));

-- populate Task_definitions table

INSERT INTO Task_definitions (task_id, task_name, task_description, task_status)
VALUES (1, 'Check in with caterers', 'Confirm catering services for event', 'Pending'),
(2, 'Set up registration desk', 'Arrange materials and check-in lists', 'Completed'),
(3, 'Keynote Speech Preparation', 'Ensure keynote speaker has necessary setup', 'In Progress'),
(4, 'Tech Equipment Setup', 'Set up microphones, projectors, and laptops', 'Completed'),
(5, 'Arrange Seating Plan', 'Organize seating for attendees', 'Pending');


-- populate Task_assignments table

INSERT INTO Task_assignments (assignment_id, task_id, event_id, attendee_id)
VALUES (1, (SELECT task_id FROM Task_definitions WHERE task_id = 1), (SELECT event_id FROM Events WHERE event_id = 1), (SELECT attendee_id FROM Attendees WHERE attendee_id = 1)),
(2, (SELECT task_id FROM Task_definitions WHERE task_id = 2), (SELECT event_id FROM Events WHERE event_id = 1), (SELECT attendee_id FROM Attendees WHERE attendee_id = 2)),
(3, (SELECT task_id FROM Task_definitions WHERE task_id = 3), (SELECT event_id FROM Events WHERE event_id = 2), (SELECT attendee_id FROM Attendees WHERE attendee_id = 3)),
(4, (SELECT task_id FROM Task_definitions WHERE task_id = 1), (SELECT event_id FROM Events WHERE event_id = 3), (SELECT attendee_id FROM Attendees WHERE attendee_id = 1)),
(5, (SELECT task_id FROM Task_definitions WHERE task_id = 2), (SELECT event_id FROM Events WHERE event_id = 3), (SELECT attendee_id FROM Attendees WHERE attendee_id = 2));
