import json
import os
from datetime import datetime
import time


TASKS_FILE = "tasks.json"


def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as file:
            tasks = json.load(file)
            return tasks
    return []


def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)


def add(new_task):
    tasks = load_tasks()
    next_id = max([task["id"] for task in tasks]) + 1
    task = {"id": next_id, "description": new_task, "status": "todo",
            "createdAt": time.time(), "updatedAt": time.time()}
    tasks.append(task)
    save_tasks(tasks)


def update(id, new_description):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == id:
            task["description"] = new_description
            task["updatedAt"] = time.time()
    save_tasks(tasks)


def delete(id):
    tasks = load_tasks()
    for index, task in enumerate(tasks):
        if task["id"] == id:
            del tasks[index]
            break
    save_tasks(tasks)


def mark_in_progress(id):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == id:
            task["status"] = "in progress"
            task["updatedAt"] = time.time()
            break
    save_tasks(tasks)


def mark_done(id):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == id:
            task["status"] = "done"
            task["updatedAt"] = time.time()
            break
    save_tasks(tasks)


def print(tasks):
    return 0


add("fifth task")
delete(3)
mark_in_progress(4)
