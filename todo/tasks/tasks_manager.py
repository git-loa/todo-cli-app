#!/usr/bin/python3

"""
tasks_manager.py - This module manages tasks
"""

from datetime import datetime
import psycopg2
from prettytable import PrettyTable, TableStyle
from ..db.database import Database


class TaskManager:
    """Class representing a task manager"""

    def __init__(self):
        """
        Initialize database instance
        """
        self.dbase = Database()

    def add_task(self, **kwargs):
        """
        Add a task
        """
        query = """
        INSERT INTO tasks(title, description, priority, due_date) \
            VALUES (%s, %s, %s, %s)
        """

        try:
            if kwargs["due_date"]:
                kwargs["due_date"] = datetime.strptime(
                    kwargs["due_date"], "%Y-%m-%d"
                ).date()
            else:
                kwargs["due_date"] = None
            params = tuple(kwargs.values())
            self.dbase.execute_query(query, "add", params)
        except psycopg2.DatabaseError as db_error:
            print(f"Error inserting into table: {db_error}")

    def dispaly_tasks(self, tasks):
        """
        Display tasks
        """
        task_table = PrettyTable()
        task_table.field_names = [
            "ID",
            "Title",
            "Description",
            "Priority",
            "Completed",
            "Created",
            "Due Date",
        ]

        for task in tasks:
            task_table.add_row(
                [task[0], task[1], task[2], task[3], task[4], task[5], task[6]]
            )
            task_table.add_divider()

        task_table.set_style(TableStyle.DOUBLE_BORDER)
        print(task_table)

    def list_task(self, status):
        """
        List tasks
        """
        query = ""
        print("\n")
        if status == "all":
            query = "SELECT * FROM tasks"
        elif status == "completed":
            query = "SELECT * FROM tasks WHERE completed = TRUE"
        elif status == "completed":
            query = "SELECT * FROM tasks WHERE completed = FALSE"

        tasks = self.dbase.fetch_query(query)

        self.dispaly_tasks(tasks)

    def update_task(self, task_id, **kwargs):
        """
        Upadate a task's attribute
        """
        set_clauses = []
        params = []

        # Iterate over the keyword arguments to build the SET clause
        for key, value in kwargs.items():
            set_clauses.append(f"{key} = %s")
            params.append(value)
        # Join the SET clauses into a single string
        set_clauses_str = ", ".join(set_clauses)

        # Build the final SQL query
        query = f"UPDATE tasks SET {set_clauses_str} WHERE task_id = %s"
        params.append(task_id)

        self.dbase.execute_query(query, "update", tuple(params))

    def delete_task(self, task_id):
        """
        Delete a task
        """
        query = "DELETE FROM tasks WHERE id = %s"
        self.dbase.execute_query(query, "delete", (task_id,))

    def close(self):
        """
        Close a connection
        """
        try:
            self.dbase.close()
        except psycopg2.OperationalError as op_error:
            print(f"Operational error: {op_error}")
        except psycopg2.DatabaseError as db_error:
            print(f"Error closing connection: {db_error}")
