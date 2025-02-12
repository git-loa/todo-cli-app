import config
import psycopg2

class Database:
    def __init__(self):
        try:
            self.conn = config.connect_db()
            self.cur = self.conn.cursor()
        except psycopg2.OperationalError as oe:
            print(f"Operational error: {oe}")
        except EnvironmentError as er:
            print(f'Environment error: {er}')
        except Exception as e:
            print(f"Exception: {e}")

    def table_exists(self, table_name):
        try:
            self.cur.execute("SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name = %s);", (table_name,))
            return self.cur.fetchone()[0]
        except (Exception, psycopg2.DatabaseError, psycopg2.DatabaseError) as error:
            print(f"Error checking if table exists: {error}")

    def execute_query(self, query, op, params=None):
        try:
            self.cur.execute(query, params)
            self.conn.commit()
            if op == "add":
                print("Task added successfully ...")
            if op == "update":
                print("Task updated successfully ...")
            if op == "delete":
                print("Task deleted.")
        except psycopg2.OperationalError as oe:
            print(f"Operational error: {oe}")
            return
        except Exception as e:
            print(f"Error during query execution: {e}")
            self.conn.rollback()
            return

    def fetch_query(self, query, params=None):
        try:
            self.cur.execute(query, params)
            rows = self.cur.fetchall()
            return rows
        except psycopg2.OperationalError as oe:
            print(f"Operational error: {oe}")
        except Exception as e:
            print(f"Error during fetch: {e}")
            return []

    def create_db_table(self, filename):
        """
        Execute an SQL fie to set up the databse schema
        """
        error = None
        try:            
            # Read the sql file
            with open(filename, 'r') as file:
                sql = file.read()
            
            # Execute the SQL commands
            self.cur.execute(sql)
            print("Table created successfully........")
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error executing SQL file: {error}")
            error = error
            return error
        
    def close(self):
        try:
            self.cur.close()
            self.conn.close()
        except psycopg2.OperationalError as oe:
            print(f"Operational error: {oe}")
        except Exception as e:
            print(f"Error closing connection: {e}")

            