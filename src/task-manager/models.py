import storage

class Task:
    def __init__(self, id, name, status, due_date=None, priority=None):
        self.id = id
        self.name = name
        self.status = status
        self.due_date = due_date
        self.priority = priority

    def edit_task(self, task):
        self.tasks[task.id] = task
        con, cur = storage.db_connection()
        
        cur.execute("UPDATE tasks SET ... WHERE .....")
        return 0

    def view_task(self, task):
        self.tasks[task.id] = task
        con, cur = storage.db_connection()

        task = cur.execute("SELECT * FROM task WHERE ....")
        return task

class TaskList:
    def __init__(self, name):
        self.name = name
        self.tasks = {}

    def create_task(self, task):
        self.tasks[task.id] = task
        con, cur = storage.db_connection()
        
        cur.execute("INSERT INTO tasks.....")
        return 0
    
    def edit_task(self, task):
        self.tasks[task.id] = task
        con, cur = storage.db_connection()
        
        cur.execute("UPDATE tasks SET ... WHERE .....")
        return 0

    def view_task(self, task):
        self.tasks[task.id] = task
        con, cur = storage.db_connection()

        task = cur.execute("SELECT * FROM task WHERE ....")
        return task
    
    def view_all_tasks(self):
        pass

    def delete_task(self, task_id):
        con, cur = storage.db_connection()

        task = cur.execute("DELETE FROM from task WHERE ....")
        self.tasks.pop(task_id, None)
        return 0