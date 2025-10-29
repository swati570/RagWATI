import requests

API_URL = "http://localhost:8080"

def register(username, password):
    res = requests.post(f"{API_URL}/register", json={"username": username, "password": password})
    return res.json()

def login(username, password):
    res = requests.post(f"{API_URL}/login", json={"username": username, "password": password})
    return res.json().get("token")
