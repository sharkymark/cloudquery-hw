-- Create a new database
CREATE DATABASE mydatabase;

-- Connect to the new database
\c mydatabase

-- Create a new table
CREATE TABLE mytable (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    email VARCHAR(100),
    started_on TIMESTAMP
);

CREATE DATABASE mydestinationdatabase;
