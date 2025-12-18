import requests
import time

BASE_URL = "http://localhost:5000"

def wait_for_app():
    for _ in range(30):
        try:
            r = requests.get(BASE_URL)
            if r.status_code == 200:
                return
        except:
            pass
        time.sleep(2)
    raise Exception("App did not start")

def test_homepage_loads():
    wait_for_app()
    r = requests.get(BASE_URL)
    assert r.status_code == 200
    assert "Favorite Movies" in r.text
