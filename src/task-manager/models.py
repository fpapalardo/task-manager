import storage

class Task:
    def __init__(self, id, name, due_date=None, priority=None):
        self.id = id
        self.name = name
        self.due_date = due_date
        self.priority = priority

class TaskList:
    def __init__(self, name):
        self.name = name
        self.tasks = {}

    def add_task(self, task):
        self.tasks[task.id] = task
        con, cur = storage.db_connection()

    def delete_task(self, task_id):
        con, cur = storage.db_connection()
        return self.tasks.pop(task_id, None)