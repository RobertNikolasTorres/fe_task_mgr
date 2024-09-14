from flask import (
    Flask,
    request,
    render_template
)
import requests

BACKEND_URL = "http://127.0.0.1:5000/tasks"

app = Flask(__name__)

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/about")
def about ():
    return render_template("about.html")

@app.get("/tasks")
def get_tasks():
    response = requests.get(BACKEND_URL)
    if response.status_code ==200:
        task_list = response.json().get("tasks")
        return render_template("list.html", tasks=task_list)
    return (
        render_template("error.html", error=response.status_code),
        response.status_code
    )

@app.get("/tasks/new/")
def task_form():
    return render_template("new.html")

@app.post("/tasks/new/")
def create_task():
    task_data = request.form
    response = requests.post(BACKEND_URL, json=task_data)
    if response.status_code ==204:
        return render_template("success.html", msg="Task created successfully")
    return (
        render_template("error.html", error= response.status_code),
        response.status_code
    )

@app.get("/tasks/<int:pk>")
def task_detail(pk):
    url = "%s/%s" % (BACKEND_URL, pk)
    response = requests.get(url)
    if response.status_code ==200:
        task_data = response.json().get("task")
        return render_template("detail.html", task=task_data)
    return (
        render_template("error.html", error=response.status_code),
        response.status_code
    )