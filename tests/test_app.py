import sys
import types

# Create lightweight stubs for modules that may not be installed in CI or dev
# so importing `app` does not fail. These provide only the symbols needed
# at import time; individual tests monkeypatch behavior further as needed.

# --- stub mysql.connector ---
mysql_mod = types.ModuleType("mysql")
mysql_connector = types.ModuleType("mysql.connector")

class _FakeMysqlError(Exception):
    pass

mysql_connector.Error = _FakeMysqlError

def _default_connect(**kwargs):
    # default will raise so code paths that expect a working connect must
    # explicitly monkeypatch this in tests
    raise _FakeMysqlError("mysql connector not configured in test environment")

mysql_connector.connect = _default_connect
mysql_mod.connector = mysql_connector

sys.modules.setdefault("mysql", mysql_mod)
sys.modules.setdefault("mysql.connector", mysql_connector)

# --- stub flask (minimal symbols for import only) ---
flask_mod = types.ModuleType("flask")

def _render_template_string(s, **kwargs):
    # Not a real Jinja2 renderer; returns the template string so tests
    # that don't rely on templating won't fail at import time.
    return s

class _FakeFlask:
    def __init__(self, name):
        self.name = name

    def route(self, path):
        def decorator(f):
            return f
        return decorator

    def run(self, *args, **kwargs):
        return None

    # test_client is not implemented here; tests avoid calling Flask test client

flask_mod.Flask = _FakeFlask
flask_mod.render_template_string = _render_template_string

sys.modules.setdefault("flask", flask_mod)

# Now import the app module (will use the stubs above if real packages are missing)
import app


def test_get_db_connection_returns_none_on_error(monkeypatch):
    """If mysql.connector.connect raises an Error, get_db_connection should return None."""

    def fake_connect(**kwargs):
        raise app.Error("connection failed")

    monkeypatch.setattr(app.mysql.connector, 'connect', fake_connect)

    conn = app.get_db_connection()
    assert conn is None


def test_get_user_data_no_connection(monkeypatch):
    """When there is no DB connection, get_user_data should return (None, [])."""

    monkeypatch.setattr(app, 'get_db_connection', lambda: None)

    name, movies = app.get_user_data()
    assert name is None
    assert movies == []


def test_get_user_data_with_fake_connection(monkeypatch):
    """When DB returns results, get_user_data should parse name and movies."""

    class FakeCursor:
        def __init__(self):
            self._last = None

        def execute(self, query):
            self._last = query

        def fetchone(self):
            if self._last and 'SELECT name' in self._last.upper():
                return {'name': 'Bob'}
            return None

        def fetchall(self):
            if self._last and 'SELECT TITLE' in self._last.upper():
                return [
                    {'title': 'Inception', 'year': 2010},
                    {'title': 'The Matrix', 'year': 1999},
                ]
            return []

        def close(self):
            return None

    class FakeConnection:
        def __init__(self):
            self._cursor = FakeCursor()

        def cursor(self, **kwargs):
            return self._cursor

        def is_connected(self):
            return True

        def close(self):
            return None

    fake_conn = FakeConnection()
    monkeypatch.setattr(app, 'get_db_connection', lambda: fake_conn)

    name, movies = app.get_user_data()
    assert name == 'Bob'
    assert isinstance(movies, list)
    assert any(m['title'] == 'Inception' for m in movies)
