import requests

API_URL = "http://localhost:8080"

def upload_pdf(token, project_id, file):
    files = {"file": file}
    data = {"project_id": project_id, "token": token}
    res = requests.post(f"{API_URL}/upload_pdf", files=files, data=data)
    return res.json()

def get_projects(token):
    res = requests.get(f"{API_URL}/my_projects", params={"token": token})
    return res.json().get("projects", [])

def ask_question(token, project_id, question):
    data = {"token": token, "project_id": project_id, "question": question}
    res = requests.post(f"{API_URL}/ask", data=data)
    return res.json().get("answer", "No answer returned")

def delete_project(token, project_id):
    res = requests.delete(f"{API_URL}/delete_project", params={"token": token, "project_id": project_id})
    return res.json()
