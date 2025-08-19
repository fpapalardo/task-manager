import storage

class Task:
    def __init__(self, id, name, status, due_date=None, priority=None, task_list_id=None):
        self.id = id
        self.name = name
        self.status = status
        self.due_date = due_date
        self.priority = priority
        self.task_list_id = task_list_id

    def save(self):
        con, cur = storage.db_connection()
        cur.execute(
            "INSERT INTO tasks (name, status, due_date, priority, task_list_id) VALUES (?, ?, ?, ?, ?)",
            (self.name, self.status, self.due_date, self.priority, self.task_list_id)
        )
        self.id = cur.lastrowid
        con.commit()
        storage.db_close_connection(con)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        con, cur = storage.db_connection()
        cur.execute(
            "UPDATE tasks SET name=?, status=?, due_date=?, priority=? WHERE id=?",
            (self.name, self.status, self.due_date, self.priority, self.id)
        )
        con.commit()
        storage.db_close_connection(con)

    def delete(self):
        con, cur = storage.db_connection()
        cur.execute("DELETE FROM tasks WHERE id=?", (self.id,))
        con.commit()
        storage.db_close_connection(con)

    @staticmethod
    def get(task_id):
        con, cur = storage.db_connection()
        row = cur.execute(
            "SELECT id, name, status, due_date, priority, task_list_id FROM tasks WHERE id=?", 
            (task_id,)
        ).fetchone()
        storage.db_close_connection(con)
        return Task(*row) if row else None


class TaskList:
    def __init__(self, name, id=None):
        self.name = name
        self.id = id
        self.tasks = []

    def save(self):
        con, cur = storage.db_connection()
        cur.execute(
            "INSERT INTO task_lists (name) VALUES (?)", 
            (self.name,)
        )
        self.id = cur.lastrowid
        con.commit()
        storage.db_close_connection(con)

    def update(self, new_name):
        self.name = new_name
        con, cur = storage.db_connection()
        cur.execute(
            "UPDATE task_lists SET name=? WHERE id=?",
            (self.name, self.id)
        )
        con.commit()
        storage.db_close_connection(con)

    def delete(self):
        con, cur = storage.db_connection()
        # First delete all tasks in this list
        cur.execute("DELETE FROM tasks WHERE task_list_id=?", (self.id,))
        # Then delete the list itself
        cur.execute("DELETE FROM task_lists WHERE id=?", (self.id,))
        con.commit()
        storage.db_close_connection(con)

    def add_task(self, task_name, due_date=None, priority=None):
        task = Task(
            id=None,
            name=task_name,
            status="pending",
            due_date=due_date,
            priority=priority,
            task_list_id=self.id
        )
        task.save()
        return task

    def get_tasks(self):
        con, cur = storage.db_connection()
        rows = cur.execute("""
            SELECT id, name, status, due_date, priority, task_list_id
            FROM tasks
            WHERE task_list_id=?
        """, (self.id,)).fetchall()
        storage.db_close_connection(con)
        return [Task(*row) for row in rows]

    @staticmethod
    def get_by_name(name):
        con, cur = storage.db_connection()
        row = cur.execute(
            "SELECT id, name FROM task_lists WHERE name=?", 
            (name,)
        ).fetchone()
        
        if not row:
            storage.db_close_connection(con)
            return None
            
        task_list = TaskList(row[1], row[0])
        
        # Fetch all tasks for this task list
        tasks = cur.execute("""
            SELECT id, name, status, due_date, priority, task_list_id
            FROM tasks
            WHERE task_list_id=?
            ORDER BY priority DESC, due_date ASC
        """, (task_list.id,)).fetchall()
        
        storage.db_close_connection(con)
        task_list.tasks = [Task(*task_row) for task_row in tasks]
        return task_list

    @staticmethod
    def get(id):
        con, cur = storage.db_connection()
        row = cur.execute(
            "SELECT id, name FROM task_lists WHERE id=?", 
            (id,)
        ).fetchone()
        
        if not row:
            storage.db_close_connection(con)
            return None
            
        task_list = TaskList(row[1], row[0])
        
        # Fetch all tasks for this task list
        tasks = cur.execute("""
            SELECT id, name, status, due_date, priority, task_list_id
            FROM tasks
            WHERE task_list_id=?
            ORDER BY priority DESC, due_date ASC
        """, (task_list.id,)).fetchall()
        
        storage.db_close_connection(con)
        task_list.tasks = [Task(*task_row) for task_row in tasks]
        return task_list
