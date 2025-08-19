from models import Task, TaskList
from storage import initial_setup

# CLI function calls into class logic
def delete_task(args):
    pass

def delete_task_list(args):
    pass

def view_task(args):
    pass

def view_task_list(args):
    task_list = TaskList(args.task_list)
    tasks = task_list.get_tasks()
    for task in tasks:
        print(f"[{task.id}] {task.name} (status: {task.status})")

def create_task(args):
    pass

def create_task_list(args):
    pass

def edit_task(args):
    pass

def edit_task_list(args):
    pass

def complete_task(args):
    pass

def init_task_manager(args):
    initial_setup()