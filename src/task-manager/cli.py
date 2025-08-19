import argparse
from main import (
    # delete functions
    delete_task_list, delete_task, 
    # view functions
    view_task_list, view_task,
    # edit functions
    edit_task_list, edit_task,
    # create functions
    create_task_list, create_task,
    # init function
    init_task_manager,
    # complete function
    complete_task
    )

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="CLI Task Manager", prog="cli-task-manager")
    subparsers = parser.add_subparsers(dest="command")

    # Parent parser for task-related settings
    task_settings_parent = argparse.ArgumentParser(add_help=False)
    task_settings_parent.add_argument("--due-date", "-d", help="Due date of the task")
    task_settings_parent.add_argument("--priority", "-p", help="Priority of the task")
    task_settings_parent.add_argument("--task-list", "-l", required=True, help="Task list name or ID")

    # Parent parser for task identification
    task_id_parent = argparse.ArgumentParser(add_help=False)
    task_id_parent.add_argument("--task-id", "-t", required=True, help="ID of the task")

    # Parent parser for task list name
    task_list_name_parent = argparse.ArgumentParser(add_help=False)
    task_list_name_parent.add_argument("name", help="Name or ID")
    
    ## CREATE ##
    create_parser = subparsers.add_parser("create", help="Create a task or task list")
    create_subparser = create_parser.add_subparsers(dest="create_type")
    
    # create task-list
    create_list_parser = create_subparser.add_parser("task-list", parents=[task_list_name_parent], help="Create a new task list")
    create_list_parser.set_defaults(func=create_task_list)
    
    # create task
    create_task_parser = create_subparser.add_parser("task", parents=[task_settings_parent, task_list_name_parent], help="Create a new task")
    create_task_parser.set_defaults(func=create_task)

    ## EDIT ##
    edit_parser = subparsers.add_parser("edit", help="Edit a task or task list information")
    edit_subparser = edit_parser.add_subparsers(dest="edit_type")
    
    # edit task-list
    edit_list_parser = edit_subparser.add_parser("task-list", parents=[task_list_name_parent], help="Edit a task list")
    edit_list_parser.add_argument("new_name", help="New name for the task list")
    edit_list_parser.set_defaults(func=edit_task_list)
    
    # edit task
    edit_task_parser = edit_subparser.add_parser("task", parents=[task_id_parent, task_settings_parent], help="Edit a task")
    edit_task_parser.set_defaults(func=edit_task)

    ## DELETE ##
    delete_parser = subparsers.add_parser("delete", help="Delete tasks or task lists")
    delete_subparser = delete_parser.add_subparsers(dest="delete_type")
    
    # delete task-list
    delete_list_parser = delete_subparser.add_parser("task-list", parents=[task_list_name_parent], help="Delete an entire task list")
    delete_list_parser.set_defaults(func=delete_task_list)
    
    # delete task
    delete_task_parser = delete_subparser.add_parser("task", parents=[task_id_parent], help="Delete a single task")
    delete_task_parser.set_defaults(func=delete_task)

    ## VIEW ##
    view_parser = subparsers.add_parser("view", help="View a task or task lists")
    view_subparser = view_parser.add_subparsers(dest="view_type")
    
    # view task-list
    view_list_parser = view_subparser.add_parser("task-list", parents=[task_list_name_parent], help="View an entire task list")
    view_list_parser.set_defaults(func=view_task_list)
    
    # view task
    view_task_parser = view_subparser.add_parser("task", parents=[task_id_parent], help="View a single task")
    view_task_parser.set_defaults(func=view_task)

    ## COMPLETE ##
    complete_parser = subparsers.add_parser("complete", help="Complete task")
    complete_subparser = complete_parser.add_subparsers(dest="complete_type")
    
    # complete task
    complete_task_parser = complete_subparser.add_parser("task", parents=[task_id_parent], help="Complete a single task")
    complete_task_parser.set_defaults(func=complete_task)

    ## INIT ##
    init_parser = subparsers.add_parser("init", help="Initialize program creating necessary DB and tables")
    init_parser.set_defaults(func=init_task_manager)

    # Parse arguments
    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()