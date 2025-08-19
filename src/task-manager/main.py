from models import Task, TaskList
from storage import initial_setup

## Helpers
def get_task_list(identifier):
    """
    Helper function to get a task list by either ID or name.
    Returns (TaskList, error_message)
    """
    if not identifier:
        return None, "No identifier provided"
    
    # Check if identifier is numeric (ID)
    if str(identifier).isdigit():
        task_list = TaskList.get(int(identifier))
        if not task_list:
            return None, f"No task list found with ID: {identifier}"
        return task_list, None
    
    # Check if identifier contains invalid characters
    if not all(c.isalnum() or c.isspace() or c in '-_' for c in identifier):
        return None, "Invalid characters in task list name"
    
    # Get by name
    task_list = TaskList.get_by_name(identifier)
    if not task_list:
        return None, f"No task list found with name: {identifier}"
    return task_list, None

def get_task(identifier):
    """
    Helper function to get a task by either ID or name.
    Returns (Task, error_message)
    """
    if not identifier:
        return None, "No identifier provided"
    
    # Check if identifier is numeric (ID)
    if str(identifier).isdigit():
        task = Task.get(int(identifier))
        if not task:
            return None, f"No task found with ID: {identifier}"
        return task, None
    
    return None, "Task lookup by name is not supported, please use task ID"

# CLI function calls into class logic
def delete_task(args):
    task, error = get_task(args.task_id)
    if error:
        print(f"Error: {error}")
        return
    
    task.delete()
    print(f"Task '{task.name}' deleted successfully")

def delete_task_list(args):
    task_list, error = get_task_list(args.task_list)
    if error:
        print(f"Error: {error}")
        return
    
    task_list.delete()
    print(f"Task list '{task_list.name}' deleted successfully")

def view_task_list(args):
    task_list, error = get_task_list(args.task_list)
    if error:
        print(f"Error: {error}")
        return
    
    print(f"\nTask List: {task_list.name} (ID: {task_list.id})")
    if not task_list.tasks:
        print("No tasks in this list")
        return
        
    for task in task_list.tasks:
        due_date = f", Due: {task.due_date}" if task.due_date else ""
        priority = f", Priority: {task.priority}" if task.priority else ""
        print(f"[{task.id}] {task.name} (Status: {task.status}{priority}{due_date})")

def view_task(args):
    task, error = get_task(args.task_id)
    if error:
        print(f"Error: {error}")
        return
    
    due_date = f", Due: {task.due_date}" if task.due_date else ""
    priority = f", Priority: {task.priority}" if task.priority else ""
    print(f"Task: {task.name} (ID: {task.id})")
    print(f"Status: {task.status}{priority}{due_date}")

def create_task(args):
    print(args)
    # task_list, error = get_task_list(args.name)
    # if task_list:
    #     print(f"Task List {args.name} already exists")
    #     return
    
    # t_list = TaskList(args.name)
    # t_list.save()

def create_task_list(args):
    task_list, error = get_task_list(args.name)
    if task_list:
        print(f"Task List {args.name} already exists")
        return
    
    t_list = TaskList(args.name)
    t_list.save()
    print("Task List created successfully")

def edit_task(args):
    task, error = get_task(args.task_id)
    if error:
        print(f"Error: {error}")
        return

def edit_task_list(args):
    task_list, error = get_task_list(args.task_list)
    if error:
        print(f"Error: {error}")
        return

def complete_task(args):
    task, error = get_task(args.task_id)
    if error:
        print(f"Error: {error}")
        return

def init_task_manager(args):
    initial_setup()