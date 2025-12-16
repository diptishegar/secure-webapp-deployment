from flask import Flask, render_template_string
import mysql.connector
from mysql.connector import Error
import os

app = Flask(__name__)


DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_NAME'),
    'port': os.getenv('DB_PORT'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD')
}

def get_db_connection():
    """Create and return a database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def get_user_data():
    """Retrieve user name and favorite movies from database"""
    connection = get_db_connection()
    if not connection:
        return None, []
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Get user name
        cursor.execute("SELECT name FROM users LIMIT 1")
        user = cursor.fetchone()
        name = user['name'] if user else "Unknown"
        
        # Get favorite movies
        cursor.execute("SELECT title, year FROM movies ORDER BY title")
        movies = cursor.fetchall()
        
        return name, movies
    
    except Error as e:
        print(f"Error querying database: {e}")
        return None, []
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/')
def index():
    """Main route to display name and favorite movies"""
    name, movies = get_user_data()
    
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Favorite Movies</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background-color: #f5f5f5;
            }
            .container {
                background-color: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 {
                color: #333;
                border-bottom: 3px solid #4CAF50;
                padding-bottom: 10px;
            }
            h2 {
                color: #555;
                margin-top: 30px;
            }
            ul {
                list-style-type: none;
                padding: 0;
            }
            li {
                background-color: #f9f9f9;
                margin: 10px 0;
                padding: 15px;
                border-left: 4px solid #4CAF50;
                border-radius: 4px;
            }
            .movie-title {
                font-weight: bold;
                color: #333;
            }
            .movie-year {
                color: #777;
                font-size: 0.9em;
            }
            .error {
                color: #d32f2f;
                padding: 10px;
                background-color: #ffebee;
                border-radius: 4px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            {% if name %}
                <h1>{{ name }}'s Favorite Movies</h1>
                
                {% if movies %}
                    <h2>Movie Collection</h2>
                    <ul>
                        {% for movie in movies %}
                            <li>
                                <span class="movie-title">{{ movie.title }}</span>
                                {% if movie.year %}
                                    <span class="movie-year">({{ movie.year }})</span>
                                {% endif %}
                            </li>
                        {% endfor %}
                    </ul>
                {% else %}
                    <p>No favorite movies found in the database.</p>
                {% endif %}
            {% else %}
                <div class="error">
                    <strong>Error:</strong> Unable to connect to the database or retrieve data.
                </div>
            {% endif %}
        </div>
    </body>
    </html>
    """
    
    return render_template_string(html_template, name=name, movies=movies)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)