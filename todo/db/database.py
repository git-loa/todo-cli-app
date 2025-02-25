#!/usr/bin/python3
"""
database.py - This module manages databse functions
"""
import psycopg2
import config


class Database:
    """
    Database class to handle connections to database
    """

    def __init__(self):
        """
        Initialize database configurations
        """
        try:
            self.conn = config.connect_db()
            self.cur = self.conn.cursor()
        except psycopg2.OperationalError as exception:
            print(f"Operational error: {exception}")
        except EnvironmentError as exception:
            print(f"Environment error: {exception}")
        except psycopg2.DatabaseError as db_error:
            print(f"Exception: {db_error}")

    def table_exists(self, table_name):
        """
        Checks if a databse table exists
        """
        try:
            self.cur.execute(
                "SELECT EXISTS(SELECT 1 FROM information_schema.tables \
                    WHERE table_name = %s);",
                (table_name,),
            )
            return self.cur.fetchone()[0]  #
        except psycopg2.DatabaseError as db_error:
            print(f"Error checking if table exists: {db_error}")
            return False

    def execute_query(self, query, sub_command, params=None):
        """
        Execute an SQL query
        """
        try:
            self.cur.execute(query, params)
            self.conn.commit()
            if sub_command == "add":
                print("Task added successfully ...")
            elif sub_command == "update":
                print(f"Task with ID {params[-1]} updated successfully ...")
            elif sub_command == "delete":
                print("Task deleted.")
            return True
        except psycopg2.OperationalError as op_error:
            print(f"Operational error: {op_error}")
            return False
        except psycopg2.DatabaseError as db_error:
            print(f"Error during query execution: {db_error}")
            self.conn.rollback()
            return False

    def fetch_query(self, query, params=None):
        """
        Handle fetch query
        """
        try:
            self.cur.execute(query, params)
            rows = self.cur.fetchall()
            return rows
        except psycopg2.OperationalError as op_error:
            print(f"Operational error: {op_error}")
            return []
        except psycopg2.DatabaseError as db_error:
            print(f"Error during fetch: {db_error}")
            return []

    def create_db_table(self, filename):
        """
        Execute an SQL file to set up the databse schema
        """

        try:
            # Read the sql file
            with open(filename, "r", encoding="utf-8") as file:
                sql = file.read()

            # Execute the SQL commands
            self.cur.execute(sql)
            print("Table created successfully........")
            self.conn.commit()
            return True
        except psycopg2.DatabaseError as db_error:
            print(f"Error executing SQL file: {db_error}")
            return False

    def close(self):
        """
        Close a connection
        """
        try:
            self.cur.close()
            self.conn.close()
        except psycopg2.OperationalError as op_error:
            print(f"Operational error: {op_error}")
        except psycopg2.DatabaseError as db_error:
            print(f"Error closing connection: {db_error}")
