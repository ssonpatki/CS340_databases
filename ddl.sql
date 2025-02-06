/*
    Course: CS340 - Introduction to Databases
    Assignment: Project Step 2 Draft - Normalized Schema + DDL with Sample Data 
    File: Data Definition Queries using Data Definition Language
    Database: SQL  
    Due Date: 6 February 2025
*/


/*
    Queries to create the tables 
*/

CREATE OR REPLACE TABLE Events (
    event_id int(11) NOT NULL UNIQUE AUTO_INCREMENT,    -- added auto_increment
    event_name varchar(255) NOT NULL UNIQUE,
    event_date date NOT NULL,
    total_attendees int(11) NOT NULL UNIQUE,
    venue_id int(11) NOT NULL,
    PRIMARY KEY (event_id),
    FOREIGN KEY(venue_id) REFERENCES Venues(venue_id)   -- added specific reference for FK
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
    task_id int(11) NOT NULL AUTO_INCREMENT,
    event_id int(11) NOT NULL UNIQUE,
    attendee_id int(11),
    PRIMARY KEY (assignment_id),
    FOREIGN KEY (task_id) REFERENCES Tasks(task_id),
    FOREIGN KEY(event_id) REFERENCES Events(event_id),
    FOREIGN KEY(attendee_id) REFERENCES Attendees(attendee_id),  -- added specific reference for FK
);

CREATE OR REPLACE TABLE Event_has_attendees (
    event_id int(11) NOT NULL UNIQUE,
    attendee_id int(11) NOT NULL,
    PRIMARY KEY (event_id, attendee_id),    -- both event_id & attendee_id are FK in step 1, make it composite key?
    FOREIGN KEY (event_id) REFERENCES Events(event_id),     -- not sure if reference is necessary
    FOREIGN KEY (attendee_id) REFERENCES Attendees(attendee_id),

);

CREATE OR REPLACE TABLE Attendees (
    attendee_id int(11) NOT NULL UNIQUE AUTO_INCREMENT,    -- added auto_increment
    first_name varchar(255) NOT NULL,
    last_name varchar(255) NOT NULL,
    email varchar(255) NOT NULL UNIQUE,
    phone_number varchar(255) NOT NULL UNIQUE,
    is_employee tinyint(1) NOT NULL DEFAULT = 0,    -- check if default is written correctly
    PRIMARY KEY (attendee_id)
);

CREATE OR REPLACE TABLE Venues (
    venue_id int(11) NOT NULL UNIQUE AUTO_INCREMENT,    -- added auto_increment
    venue_name varchar(255) NOT NULL,
    capacity int(11) NOT NULL,
    is_employee tinyint(1) NOT NULL DEFAULT = 1,
    PRIMARY KEY (venue_id)
);


/*
    Queries to insert data 
    Note: (SELECT <attribute_name> FROM <table_name> WHERE <attribute_name> ='') is used 
    when attribute it a FK
*/

-- populate Events table 

INSERT INTO Events (event_id, event_name, event_date, total_attendees, venue_id)
VALUES ('int', 'varchar', 'date', 'int', (SELECT venue_id FROM Venues WHERE venue_id =''));

-- populate Task_definitions table

INSERT INTO Tasks (task_id, task_name, task_description, task_status)
VALUES ('task-id', 'task-name', 'task_des', 'status');

-- populate Task_assignments table

INSERT INTO Tasks (assignment_id, task_id, event_id, attendee_id)
VALUES ('assignment-id', (SELECT task_id FROM Task_definitions WHERE task_id =''), (SELECT event_id FROM Events WHERE event_id =''), 
(SELECT attendee_id FROM Attendees WHERE attendee_id =''));

-- populate Event_has_attendees intersection table

INSERT INTO Event_has_attendees (event_id, attendee_id)
VALUES ((SELECT event_id FROM Events WHERE event_id =''), (SELECT attendee_id FROM Attendees WHERE attendee_id =''));

-- populate Attendees table

INSERT INTO Attendees (attendee_id, first_name, last_name, event_date, email, phone_number, is_employee)
VALUES ();

-- populate Venues table

INSERT INTO Venues (venue_id, venue_name, capacity, is_employee)
VALUES ();
