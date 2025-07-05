"""This application is CLI Task Tracker."""
import json
import os
from datetime import datetime
import time
import argparse

# name of the data base file
TASKS_FILE = "tasks.json"


def load_tasks():
    """initilizing file. creates one if it does not exist."""
    if os.path.exists(TASKS_FILE):
        try:
            with open(TASKS_FILE, "r", encoding="utf-8") as file:
                tasks = json.load(file)
                return tasks
        except json.JSONDecodeError:
            print("Warning: Could not decode tasks.json. Starting fresh.")
    return []


def save_tasks(tasks):
    """Saves list of tasks into the database file."""
    with open(TASKS_FILE, 'w', encoding="utf-8") as file:
        json.dump(tasks, file, indent=4)


def task_search(task_found, task_id):
    """This function prints error message if there is no task with the ID in Database."""
    if task_found is False:
        print(f"Task with ID:{task_id} not found.")


def add_task(new_task):
    """Adds a new task to the tasks list."""
    tasks = load_tasks()
    if len(tasks) > 0:
        next_id = max([task["id"] for task in tasks]) + 1
    else:
        next_id = 1
    task = {"id": next_id, "description": new_task, "status": "todo",
            "createdAt": time.time(), "updatedAt": time.time()}
    tasks.append(task)
    print(
        f"Task added: {task['description']} (ID:{task['id']}) ")
    save_tasks(tasks)


def update_task(task_id, new_description):
    """Updates a task with the ID"""
    tasks = load_tasks()
    task_found = False
    for task in tasks:
        if task["id"] == task_id:
            task["description"] = new_description
            task["updatedAt"] = time.time()
            task_found = True
            print(
                f"Task updated: {task['description']} (ID:{task['id']}) ")
            break
    task_search(task_found, task_id)
    save_tasks(tasks)


def delete_task(task_id):
    """Deletes a task from the files using the ID"""
    tasks = load_tasks()
    task_found = False
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            del tasks[index]
            task_found = True
            print(
                f"Task deleted: {task['description']} (ID:{task['id']}) ")
            break
    task_search(task_found, task_id)
    save_tasks(tasks)


def mark_in_progress(task_id):
    """Marks a task as in-progress status"""
    tasks = load_tasks()
    task_found = False
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "in-progress"
            task["updatedAt"] = time.time()
            task_found = True
            print(
                f"Task marked in-progress: {task['description']} (ID:{task['id']}) ")
            break
    task_search(task_found, task_id)
    save_tasks(tasks)


def mark_done(task_id):
    """Marks a task as done status"""
    tasks = load_tasks()
    task_found = False
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "done"
            task["updatedAt"] = time.time()
            task_found = True
            print(
                f"Task marked done: {task['description']} (ID:{task['id']}) ")
            break
    task_search(task_found, task_id)
    save_tasks(tasks)


def print_tasks(sort=None):
    """Prints out all task or tasks based on the status."""
    tasks = load_tasks()
    if sort:
        tasks = [task for task in tasks if task["status"] == sort]
        print(f"Tasks with status '{sort}':")
    else:
        print("All Tasks.")

    print(f"{'ID':<5} {'Task Description':<65} {'Status':<12} {'Created At':<20}")
    print("-" * 120)

    for task in tasks:
        dt = datetime.fromtimestamp(task["createdAt"])
        print(
            f"{task["id"]:<5} {task["description"]:<65} {task["status"]:<12} {dt}")


def main():
    """main function doing the CLI arguments."""
    parser = argparse.ArgumentParser(description="Task CLI App")
    subparsers = parser.add_subparsers(dest="command")

    # Add task
    add = subparsers.add_parser("add", help="Add a new task.")
    add.add_argument("description", type=str, help="Description of the task.")

    # Update task
    update = subparsers.add_parser(
        "update", help="Update the task with its id.")
    update.add_argument("id", type=int, help="The id of the task.")
    update.add_argument("new_description", type=str,
                        help="The new description for the task.")

    # Delete task
    delete = subparsers.add_parser("delete", help="Delete a task.")
    delete.add_argument("id", type=int, help="ID of the task to delete.")

    # mark-in-progress
    markinprogress = subparsers.add_parser(
        "mark-in-progress", help="Mark a task to in-progress status.")
    markinprogress.add_argument("id", type=int, help="ID of the task to mark.")

    # mark-done
    markdone = subparsers.add_parser(
        "mark-done", help="Mark a task to done status.")
    markdone.add_argument("id", type=int, help="ID of the task to mark.")

    # List tasks
    list_parser = subparsers.add_parser(
        "list", help="List tasks (optionally sorted)")
    list_parser.add_argument(
        "list_by",
        type=str,
        nargs="?",
        choices=["done", "todo", "in-progress"],
        help="List tasks filtered by status: done, todo, progress"
    )

    args = parser.parse_args()

    if args.command == "add":
        add_task(args.description)
    elif args.command == "delete":
        delete_task(args.id)
    elif args.command == "update":
        update_task(args.id, args.new_description)
    elif args.command == "mark-in-progress":
        mark_in_progress(args.id)
    elif args.command == "mark-done":
        mark_done(args.id)
    elif args.command == "list":
        if args.list_by is None:
            print_tasks()
        else:
            print_tasks(args.list_by)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
