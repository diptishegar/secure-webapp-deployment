CREATE DATABASE IF NOT EXISTS testdb;
USE testdb;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50)
);

CREATE TABLE movies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100),
    year INT
);

INSERT INTO users (name) VALUES ('Dipti');

INSERT INTO movies (title, year) VALUES
('Interstellar', 2014),
('Inception', 2010);
