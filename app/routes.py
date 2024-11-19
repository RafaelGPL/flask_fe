from flask import (
    Flask,
    request as flask_request,
    render_template
)

import requests

BACKEND_URL = "http://127.0.0.1:5000/tasks"
app = Flask(__name__)

@app.get("/")
def index():
    return render_template("home.html")

@app.get("/about")
def about():
    return render_template("about.html")

@app.get("/tasks")
def view_tasks():
    response = requests.get(BACKEND_URL)
    if response.status_code == 200:
        task_list = response.json().get("tasks")
        return render_template("list.html", tasks=task_list)
    return (
        render_template("error.html", err_code=response.status_code),
        response.status_code
    )

@app.get("/tasks/edit/<int:pk>/")
def edit_form(pk):
    url = "%s/%s" % (BACKEND_URL, pk)
    response = requests.get(url)
    if response.status_code == 200:
        task_data = response.json().get("task")
        return render_template("edit.html", task=task_data)
    return (
        render_template("error.html", err_code=response.status_code),
        response.status_code
    )
# {{ url_for('edit_task', pk=task['id']) }}
@app.post("/tasks/edit/<int:pk>/")
def edit_task(pk):
    url = "%s/%s" % (BACKEND_URL, pk)
    response = requests.put(url, json=flask_request.form)
    if response.status_code == 204:
        return render_template("success.html", message="Task edit succeeded")
    return (
        render_template("error.html", err_code=response.status_code),
        response.status_code
    )