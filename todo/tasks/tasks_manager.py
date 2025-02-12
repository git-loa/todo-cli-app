from ..db.database import Database
from prettytable import PrettyTable, TableStyle
import psycopg2
from datetime import datetime

class TaskManager:
    def __init__(self):
        self.db = Database()

    def add_task(self, title, description=None, priority=None, due_date=None):
        query = """
        INSERT INTO tasks(title, description, priority, due_date) VALUES (%s, %s, %s, %s)
        """
        try:
            due_date = datetime.strptime(due_date, "%Y-%m-%d").date() if due_date else None
            params = (title, description, priority, due_date)
            self.db.execute_query(query, "add", params)
        except Exception as e:
            print(f"Error inserting into table: {e}")

    def dispaly_tasks(self, tasks):
        task_table = PrettyTable()
        task_table.field_names = ["ID", "Title", "Description", "Priority", "Completed", "Created", "Due Date"]

        for task in tasks:
            task_table.add_row([task[0], task[1], task[2], task[3], task[4], task[5], task[6]])
            task_table.add_divider()
            
        task_table.set_style(TableStyle.DOUBLE_BORDER)
        print(task_table)

    def list_task(self, status):
        print('\n')
        if status == "all":
            query = 'SELECT * FROM tasks'
        elif status == "completed":
            query = 'SELECT * FROM tasks WHERE completed = TRUE'
        elif status == "completed":
            query = 'SELECT * FROM tasks WHERE completed = FALSE'
        
        tasks = self.db.fetch_query(query)

        self.dispaly_tasks(tasks)

    def update_task(self, task_id, title = None, description = None, completed = None, priority=None, due_date = None):
        query = 'UPDATE tasks SET '
        params = []
        if title:
            query += 'title = %s, '
            params.append(title)
        
        if description:
            query += 'description = %s, '
            params.append(description)
        
        if completed:
            query += 'completed = %s, '
            params.append(completed)

        if priority:
            query += 'priority = %s, '
            params.append(priority)

        if due_date:
            query += 'due_date = %s, '
            params.append(due_date)

        query = query.rstrip(', ')
        query += ' WHERE id = %s'

        params.append(task_id)

        self.db.execute_query(query, "update", tuple(params))

    def delete_task(self, task_id):
        query = 'DELETE FROM tasks WHERE id = %s'
        self.db.execute_query(query, "delete", (task_id,))

    def close(self):
        try:
            self.db.close()
        except psycopg2.OperationalError as oe:
            print(f"Operational error: {oe}")
        except Exception as e:
            print(f"Error closing connection: {e}")
