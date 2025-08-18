import argparse
from main import (
    # delete functions
    delete_task_list, delete_task, 
    # view functions
    view_task_list, view_task,
    # edit functions
    edit_task_list, edit_task,
    # create functions
    create_task_list, create_task
    )

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="CLI Task Manager", prog="cli-task-manager")
    subparsers = parser.add_subparsers(dest="command")

    # Used with all commands to interact with the correct Task and Task List
    task_list_parent = argparse.ArgumentParser(add_help=False)
    task_list_parent.add_argument("task_list", help="Name or ID of the Task List")

    # Used with create and edit
    task_settings_parent = argparse.ArgumentParser(add_help=False)
    task_settings_parent.add_argument("--due-date", "-d", required=False, help="Due date of the task")
    task_settings_parent.add_argument("--prority", "-p", type=str, required=False, help="Priority of the task")

    # Used with Edit, Delete and View
    task_alter_parent = argparse.ArgumentParser(add_help=False)
    task_alter_parent.add_argument("--task-id", "-t", required=False, help="ID of the task")

    ## CREATE ##
    # 'create' command
    create_parser = subparsers.add_parser("create", help="Create a task or task list")
    create_subparser = create_parser.add_subparsers(dest="create_type")
    # create task list
    create_list_parser = create_subparser.add_parser(
        "task-list", parents=[task_list_parent], help="Create a new task list"
    )
    create_list_parser.set_defaults(func=create_task_list)
    # create task
    create_task_parser = create_subparser.add_parser(
        "task", parents=[task_list_parent, task_alter_parent, task_settings_parent], help="Create a new task"
    )
    create_task_parser.set_defaults(func=create_task)

    ## EDIT ##
    # 'edit' command
    edit_parser = subparsers.add_parser("edit", help="Edit a task or task list information")
    edit_subparser = edit_parser.add_subparsers(dest="edit_type")
    # edit task list
    edit_list_parser = edit_subparser.add_parser(
        "task-list", parents=[task_list_parent], help="Edit a task list"
    )
    edit_list_parser.set_defaults(func=edit_task_list)
    # edit task
    edit_task_parser = edit_subparser.add_parser(
        "task", parents=[task_list_parent, task_alter_parent, task_settings_parent], help="Edit a task"
    )
    edit_task_parser.set_defaults(func=edit_task)

    ## DELETE ##
    # 'delete' command
    delete_parser = subparsers.add_parser("delete", help="Delete tasks or task lists")
    delete_subparser = delete_parser.add_subparsers(dest="delete_type")
    # delete task list
    delete_list_parser = delete_subparser.add_parser(
        "task-list", parents=[task_list_parent], help="Delete an entire task list"
    )
    delete_list_parser.set_defaults(func=delete_task_list)
    # delete task
    delete_task_parser = delete_subparser.add_parser(
        "task", parents=[task_list_parent, task_alter_parent], help="Delete a single task"
    )
    delete_task_parser.set_defaults(func=delete_task)

    ## VIEW ##
    # 'view' command
    view_parser = subparsers.add_parser("view", help="View a task or task lists")
    view_subparser = view_parser.add_subparsers(dest="view_type")
    # view task list
    view_list_parser = view_subparser.add_parser(
        "task-list", parents=[task_list_parent], help="View an entire task list"
    )
    view_list_parser.set_defaults(func=view_task_list)
    # view task
    view_task_parser = view_subparser.add_parser(
        "task", parents=[task_list_parent, task_alter_parent], help="View a single task"
    )
    view_task_parser.set_defaults(func=view_task)

    # Parse arguments
    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()