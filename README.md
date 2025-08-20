# CLI Task Manager

A command-line task management tool that helps you organize tasks in lists, set priorities, and track due dates.

## Features

- Create and manage multiple task lists
- Add tasks with priorities and due dates
- Mark tasks as complete
- View tasks by list or individually
- Edit task details
- Delete tasks and task lists

## Installation

1. Clone the repository:
```bash
git clone https://github.com/fpapalardo/task-manager.git
cd task-manager
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Initialize the Task Manager
```bash
python src/task-manager/cli.py init
```

### Task Lists
```bash
# Create a task list
python src/task-manager/cli.py create task-list "My List"

# View a task list
python src/task-manager/cli.py view task-list "My List"

# Edit task list name
python src/task-manager/cli.py edit task-list "My List" "New List Name"

# Delete a task list
python src/task-manager/cli.py delete task-list "My List"
```

### Tasks
```bash
# Create a task
python src/task-manager/cli.py create task "Buy milk" --task-list "My List" --priority high --due-date "2023-12-31"

# View a task
python src/task-manager/cli.py view task --task-id 1 --task-list "My List"

# Edit a task
python src/task-manager/cli.py edit task --task-id 1 --priority medium --task-list "My List"

# Complete a task
python src/task-manager/cli.py complete task --task-id 1 --task-list "My List"

# Delete a task
python src/task-manager/cli.py delete task --task-id 1 --task-list "My List"
```

## Project Structure

```
cli-productivity-tool/
├── src/
│   └── task-manager/
│       ├── __init__.py
│       ├── cli.py          # Command-line interface
│       ├── main.py         # Main application logic
│       ├── models.py       # Data models
│       └── storage.py      # Database operations
├── tests/
│   └── test_tasks.py       # Unit tests
├── requirements.txt
└── README.md
```

## Development

### Running Tests

To run all tests:
```bash
python -m unittest -v tests/test_tasks.py
```

To run a specific test:
```bash
python -m unittest -v tests/test_tasks.py -k <test_name>
```

### Database

The application uses SQLite for data storage. The database file (`tasks_manager.db`) is created automatically when you run the initialization command.

Tables:
- `task_lists`: Stores task list information
- `tasks`: Stores task details with foreign key to task lists

## Task Properties

- **Name**: Task description
- **Priority**: low, medium, high (optional)
- **Due Date**: YYYY-MM-DD format (optional)
- **Status**: pending or completed

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.