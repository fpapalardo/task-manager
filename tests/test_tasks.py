import unittest
import sys
import os
from datetime import datetime
import sqlite3

# Add the src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src', 'task-manager'))

from models import Task, TaskList
from storage import initial_setup
import storage

class TestTaskManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Initialize test database"""
        print("\nSetting up test suite...")
        storage.DB_NAME = "test_tasks_manager.db"
        storage.reset_database()
        storage.initial_setup()

    @classmethod
    def tearDownClass(cls):
        """Clean up test database"""
        print("\nCleaning up test suite...")
        storage.reset_database()

    def setUp(self):
        """Setup before each test"""
        con, cur = storage.db_connection()
        try:
            cur.execute("DELETE FROM tasks")
            cur.execute("DELETE FROM task_lists")
            con.commit()
        finally:
            storage.db_close_connection(con)
        
        self.task_list = TaskList("Test List")
        self.task_list.save()

    def tearDown(self):
        """Clean up after each test"""
        con, cur = storage.db_connection()
        try:
            cur.execute("DELETE FROM tasks")
            cur.execute("DELETE FROM task_lists")
            con.commit()
        finally:
            storage.db_close_connection(con)

    # Task List Creation Tests
    def test_create_task_list(self):
        """Test creating a task list"""
        task_list = TaskList("Shopping List")
        task_list.save()
        
        retrieved = TaskList.get_by_name("Shopping List")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.name, "Shopping List")

    def test_create_duplicate_task_list(self):
        """Test creating a task list with existing name"""
        # First creation
        task_list1 = TaskList("Shopping List")
        task_list1.save()
        
        # Verify first creation
        self.assertIsNotNone(TaskList.get_by_name("Shopping List"))
        
        # Attempt duplicate creation should raise IntegrityError
        task_list2 = TaskList("Shopping List")
        with self.assertRaises(sqlite3.IntegrityError):
            task_list2.save()
        
        # Verify only one exists
        con, cur = storage.db_connection()
        count = cur.execute("SELECT COUNT(*) FROM task_lists WHERE name=?", ("Shopping List",)).fetchone()[0]
        storage.db_close_connection(con)
        self.assertEqual(count, 1)

    # Task Creation Tests
    def test_create_task_basic(self):
        """Test creating a basic task"""
        task = self.task_list.add_task("Buy milk")
        self.assertIsNotNone(task.id)
        self.assertEqual(task.name, "Buy milk")
        self.assertEqual(task.status, "pending")
        self.assertEqual(task.task_list_id, self.task_list.id)

    def test_create_task_with_details(self):
        """Test creating a task with all optional parameters"""
        due_date = "2025-12-31"
        task = self.task_list.add_task(
            "Buy bread",
            due_date=due_date,
            priority="high"
        )
        self.assertEqual(task.due_date, due_date)
        self.assertEqual(task.priority, "high")
        self.assertEqual(task.task_list_id, self.task_list.id)

    # Task List View Tests
    def test_view_empty_task_list(self):
        """Test viewing an empty task list"""
        retrieved = TaskList.get(self.task_list.id)
        self.assertEqual(len(retrieved.tasks), 0)

    def test_view_task_list_with_tasks(self):
        """Test viewing a task list with multiple tasks"""
        # Add tasks
        task1 = self.task_list.add_task("Task 1")
        task2 = self.task_list.add_task("Task 2", priority="high")
        
        # Retrieve and verify
        retrieved = TaskList.get(self.task_list.id)
        self.assertEqual(len(retrieved.tasks), 2)
        
        # Find task2 by id since order is by id
        found_task = next(t for t in retrieved.tasks if t.id == task2.id)
        self.assertEqual(found_task.priority, "high")

    def test_view_all_task_lists(self):
        """Test viewing all task lists"""
        # Create additional task lists
        TaskList("List 2").save()
        TaskList("List 3").save()
        
        # Retrieve all
        all_lists = TaskList.get_all()
        self.assertEqual(len(all_lists), 3)

    # Task View Tests
    def test_view_task_details(self):
        """Test viewing detailed task information"""
        task = self.task_list.add_task(
            "Complex task",
            due_date="2025-01-01",
            priority="medium"
        )
        
        retrieved = Task.get(task.id)
        self.assertEqual(retrieved.name, "Complex task")
        self.assertEqual(retrieved.due_date, "2025-01-01")
        self.assertEqual(retrieved.priority, "medium")
        self.assertEqual(retrieved.status, "pending")

    # Edit Tests
    def test_edit_task_partial(self):
        """Test editing only some task properties"""
        task = self.task_list.add_task("Original task")
        
        # Update only priority
        task.update(priority="high")
        
        updated = Task.get(task.id)
        self.assertEqual(updated.name, "Original task")  # Unchanged
        self.assertEqual(updated.priority, "high")       # Changed

    def test_edit_task_list_name(self):
        """Test editing task list name"""
        self.task_list.update("New List Name")
        
        updated = TaskList.get(self.task_list.id)
        self.assertEqual(updated.name, "New List Name")

    # Status Tests
    def test_task_status_workflow(self):
        """Test complete task workflow"""
        task = self.task_list.add_task("Test task")
        
        # Verify initial status
        self.assertEqual(task.status, "pending")
        
        # Complete task
        task.update(status="completed")
        
        # Verify completion
        updated = Task.get(task.id)
        self.assertEqual(updated.status, "completed")

    # Delete Tests
    def test_cascade_delete(self):
        """Test that deleting a task list deletes its tasks"""
        # Create tasks
        self.task_list.add_task("Task 1")
        self.task_list.add_task("Task 2")
        
        # Delete list
        self.task_list.delete()
        
        # Verify all related tasks are deleted
        con, cur = storage.db_connection()
        task_count = cur.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
        storage.db_close_connection(con)
        self.assertEqual(task_count, 0)

    # Error Cases
    def test_invalid_operations(self):
        """Test various invalid operations"""
        # Non-existent task
        self.assertIsNone(Task.get(999))
        
        # Non-existent task list
        self.assertIsNone(TaskList.get(999))
        
        # Invalid task list name
        self.assertIsNone(TaskList.get_by_name("Invalid@Name"))
        
        # Invalid priority
        task = self.task_list.add_task("Test task")
        with self.assertRaises(ValueError):
            task.update(priority="INVALID")

if __name__ == '__main__':
    unittest.main()