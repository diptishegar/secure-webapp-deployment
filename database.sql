CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE movies (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    year INT
);

-- Insert sample data
INSERT INTO users (name) VALUES ('John Doe');

INSERT INTO movies (title, year) VALUES 
    ('The Shawshank Redemption', 1994),
    ('The Godfather', 1972),
    ('Inception', 2010),
    ('Pulp Fiction', 1994);

DROP USER IF EXISTS 'admin'@'%';
DROP USER IF EXISTS 'admin'@'localhost';

-- Create admin user with % wildcard (allows connections from any host)
CREATE USER 'admin'@'%' IDENTIFIED BY 'admin123';

-- Grant all privileges on movies_db database
GRANT ALL PRIVILEGES ON movies_db.* TO 'admin'@'%';

-- Apply changes
FLUSH PRIVILEGES;

-- Verify the user was created
SELECT user, host FROM mysql.user WHERE user='admin';
