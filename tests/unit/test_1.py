import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import app
from mysql.connector import Error
from unittest.mock import patch, MagicMock

def test_get_db_connection_success():
    with patch("mysql.connector.connect") as mock_connect:
        mock_connect.return_value = MagicMock()
        conn = app.get_db_connection()
        assert conn is not None



@patch("mysql.connector.connect", side_effect=Error("DB down"))
def test_get_db_connection_failure(mock_connect):
    conn = app.get_db_connection()
    assert conn is None



def test_get_user_data_no_connection():
    with patch("app.get_db_connection", return_value=None):
        name, movies = app.get_user_data()
        assert name is None
        assert movies == []


def test_index_route_client():
    app.app.testing = True
    client = app.app.test_client()

    with patch("app.get_user_data", return_value=("Dipti", [])):
        response = client.get("/")
        assert response.status_code == 200
        assert b"Dipti" in response.data
