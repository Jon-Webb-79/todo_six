# Import necessary packages here
import sys
import uuid
from datetime import datetime, timedelta

import pandas as pd
from PyQt6.QtSql import QSqlDatabase, QSqlQuery

# ==========================================================================================
# ==========================================================================================

# File:    database.py
# Date:    June 04, 2023
# Author:  Jonathan A. Webb
# Purpose: This file contains classes that implement local and shared databases for the
#          PyQt6 library
# ==========================================================================================
# ==========================================================================================
# Insert Code here


class SQLiteManager(QSqlDatabase):
    """
    Class to manage generic SQLite functions

    :param db_name: The name and pathlength to the SQLite database
    :param connection_name: A unique name for the database connection to distinguish
                            it from other connections
    :param hostname: The hostname for the database, set to None for SQLite
    :param username: The username for database access, set to None for SQLite
    :param pwd: The password associated with the username, set to None for SQLite

    The SQLiteManager code examples assumes the existence of a SQLite database named
    'data.db' which contains a table named 'inventory' with the following structure:

    +----+---------+--------+
    | ID | Product | Number |
    +----+---------+--------+
    |  1 | A       |   10.0 |
    +    +         +        +
    |  2 | B       |   15.5 |
    +    +         +        +
    |  3 | C       |   20.0 |
    +    +         +        +
    |  4 | D       |   25.5 |
    +    +         +        +
    |  5 | E       |   30.0 |
    +----+---------+--------+

    'ID' is an integer primary key, 'Product' is a text entry, and 'Number' is a real
    number.

    """

    def __init__(
        self,
        db_name: str,
        connection_name: str = None,
        hostname: str = None,
        username: str = None,
        pwd: str = None,
    ):
        msg = "Hostname, Username, and Password are no required in SQLite\n"
        if hostname is not None or username is not None or pwd is not None:
            sys.stderr.write(msg)
        if connection_name is None:
            connection_name = str(uuid.uuid4())  # use a UUID as a unique connection name
        self.db_name = db_name
        self.con = self.addDatabase("QSQLITE", connection_name)
        self.con.setDatabaseName(db_name)
        super().__init__()

    # ------------------------------------------------------------------------------------------

    def open_db(self) -> tuple[bool, str]:
        """
        Method to open an existing database.

        :return result: A tuple containing a boolean and a string.  A boolean of
                        True indicates the operation was successful, and the string
                        contains a description of the result


        Example:

        .. code-block::

            from todo_six.database import SQLiteManager

            # example for class instantiation
            db_manager = SQLiteManager('data.db')
            success, message = db_manager.open_db()
            print(success)
            print(message)

            db_manager.close_db()
            >> True
            >> data.db database successfully opened

        """
        if not self.con.open():
            # Write to stderr for debugging
            sys.stderr.write(f"{self.db_name} database does not exist\n")
            return False, f"{self.db_name} database does not exist"
        return True, f"{self.db_name} database sucessfully opened"

    # ------------------------------------------------------------------------------------------

    def close_db(self) -> tuple[bool, str]:
        """
        Method to close a database connection

        :return result: A tuple containing a boolean and a string.  A boolean of
                        True indicates the operation was successful, and the string
                        contains a description of the result

        Example:

        .. code-block::

            from todo_six.database import SQLiteManager

            # example for class instantiation
            db_manager = SQLiteManager('data.db')
            success, message = db_manager.open_db()
            print(success)
            print(message)

            success, message = db_manager.close_db()
            >> True
            >> data.db database successfully opened

            >> True
            >> data.db database successfully closed
        """
        if not self.con.isOpen():
            # Write to stderr for debugging
            sys.stderr.write(f"{self.db_name} database is not open\n")
            return False, f"{self.db_name} database is not open"
        self.con.close()
        return True, f"{self.db_name} database succesfully closed"

    # ------------------------------------------------------------------------------------------

    def db_query(self, query: str, params: tuple = None) -> tuple[bool, QSqlQuery, str]:
        """
        Method to query a database

        :param query: A string query of a database
        :param params: A tuple containing parameters to be included in the query
        :return result: A tuple containing a boolean, a QSqlQuery object, and a string.
                        The boolean indicates the operation was successful,
                        the QSqlQuery object contains the query results (if any),
                        and the string contains a description of the result.

        .. code-block::

            from todo_six.database import SQLiteManager

            # Example for class instantiation
            db_manager = SQLiteManager('data.db')
            success, message = db_manager.open_db()
            print(success)
            print(message)

            # - Example 1: Execute UPDATE statement with parameters
            #  (does not return QSqlQuery object)
            query = "UPDATE inventory SET Number = ? WHERE Product = ?;"
            params = (50, 'A')
            success, result, message = db_manager.db_query(query, params)
            if success:
                print(message)
            else:
                print("Update failed:", message)

            # Example 2: Execute SELECT statement (returns QSqlQuery object)
            query = "SELECT * FROM inventory WHERE Product = ?;"
            params = ('A', )
            success, result, message = db_manager.db_query(query, params)
            ids = []
            products = []
            numbers = []
            if success:
                print("Query successful!")
                while result.next():
                    ids.append(result.value(0))
                    products.append(result.value(1))
                    numbers.append(result.value(2))
            print(f"ID: {id}, Product: {product}, Number: {number}")
            else:
                print("Query failed:", message)

            db_manager.close_db()
        """
        if not self.con.isOpen():
            # Write to stderr for debugging
            sys.stderr.write(f"{self.db_name} database is not open\n")
            return False, QSqlQuery(), f"{self.db_name} database is not open"

        q = QSqlQuery(self.con)

        q.prepare(query)

        if params is not None:
            for param in params:
                q.addBindValue(param)

        success = q.exec()

        if not success:
            error_message = q.lastError().text()
            sys.stderr.write(f"Error executing query: {error_message}\n")
            return False, QSqlQuery(), f"Error executing query: {error_message}"

        return True, q, f"Query executed successfully on {self.db_name} database"

    # ------------------------------------------------------------------------------------------

    def table_schema(self, table_name: str) -> tuple[bool, dict[str, str], str]:
        """
        Method to return the column names and datatypes for a table

        :param table_name: The name of the table
        :return result: A tuple containing a boolean and a dictionary. A boolean of
                        True indicates the operation was successful, and the dictionary
                        contains the names of each column and the type associated with
                        each column
        Example:

        .. code-block::

            from todo_six.database import SQLiteManager

            # example for class instantiation
            db_manager = SQLiteManager('data.db')
            success, message = db_manager.open_db()

            success, schema, message = db_manager.table_schema('inventory')
            if success:
                print(schema)
            else:
                print(message)

            db_manager.close_db()

            >> {'ID': 'INTEGER', 'Product': 'TEXT', 'Number': 'REAL'}

        """
        if not self.con.isOpen():
            sys.stderr.write(f"{self.db_name} database is not open\n")
            return False, {}, f"{self.db_name} database is not open"

        query = QSqlQuery(self.con)
        query_str = f"PRAGMA table_info({table_name})"
        query.exec(query_str)

        result = {}
        while query.next():
            column_name = query.value("name")
            column_type = query.value("type")
            result[column_name] = column_type

        return True, result, f"{self.db_name} queried for {table_name} schema"

    # ------------------------------------------------------------------------------------------

    def db_schema(self) -> tuple[bool, dict[str, dict[str, str]], str]:
        """
        Method to return the column names and datatypes for all tables in the database.

        :return result: A tuple containing a boolean and a nested dictionary. A boolean
                        of True indicates the operation was successful, and the nested
                        dictionary contains the names of each table as keys, each
                        containing a dictionary of column names and the type associated
                        with each column. The string is a description of the result.

        Example:

        .. code-block::

            from todo_six.database import SQLiteManager

            # example for class instantiation
            db_manager = SQLiteManager('data.db')
            success, message = db_manager.open_db()

            success, schema, message = db_manager.db_schema()
            if success:
                print(schema)
            else:
                print(message)

            db_manager.close_db()

            >> {'inventory': {'ID': 'INTEGER', 'Product': 'TEXT', 'Number': 'REAL'}}

        """
        if not self.con.isOpen():
            sys.stderr.write(f"{self.db_name} database is not open\n")
            return False, {}, f"{self.db_name} database is not open"

        table_query = QSqlQuery(self.con)
        table_query.exec("SELECT name FROM sqlite_master WHERE type='table';")

        result = {}
        while table_query.next():
            table_name = table_query.value("name")
            column_query = QSqlQuery(self.con)
            column_query.exec(f"PRAGMA table_info({table_name})")
            table_schema = {}
            while column_query.next():
                column_name = column_query.value("name")
                column_type = column_query.value("type")
                table_schema[column_name] = column_type
            result[table_name] = table_schema

        return True, result, f"{self.db_name} database schema queried"

    # ------------------------------------------------------------------------------------------

    def create_table(
        self, table_name: str, column_names: list[str], data_types: list[str]
    ) -> tuple[bool, str]:
        """
         Method to create a table in the database.

         :param table_name: The name of the table
         :param column_names: A list of the names of columns
         :param data_types: A list of data types for each column
         :return: A tuple containing a boolean and a string. A boolean of
                  True indicates the operation was successful, and the string
                  contains a description of the result

        Example:

         .. code-block::

             from todo_six.database import SQLiteManager

             # example for class instantiation
             db_manager = SQLiteManager('data.db')
             success, message = db_manager.open_db()

             success, message = db_manager.create_table('new_table',
                               ['ID', 'Name', 'Age'],
                               ['INTEGER', 'TEXT', 'INTEGER'])
             if success:
                 print(f"Successfully created table: {message}")
             else:
                 print(f"Failed to create table: {message}")

             db_manager.close_db()

             >> Successfully created table: Table new_table successfully created

        """
        if not self.con.isOpen():
            sys.stderr.write(f"{self.db_name} database is not open\n")
            return False, f"{self.db_name} database is not open"

        if len(column_names) != len(data_types):
            return False, "Column names and data types lists must be of same length"

        column_query_parts = [
            f"{name} {type}" for name, type in zip(column_names, data_types)
        ]
        column_query = ", ".join(column_query_parts)
        query_str = f"CREATE TABLE {table_name} ({column_query});"

        query = QSqlQuery(self.con)
        query.exec(query_str)

        msg = f"Failed to create table {table_name}: {query.lastError().text()}"
        if query.lastError().isValid():
            return False, msg

        return True, f"Table {table_name} successfully created"

    # ------------------------------------------------------------------------------------------

    def table_exists(self, table_name: str) -> tuple[bool, str]:
        """
        Method to check if a table exists in the database

        :param table_name: The name of the table
        :return: True if the table exists, False otherwise
        """
        if not self.con.isOpen():
            sys.stderr.write(f"{self.db_name} database is not open\n")
            return False, f"{self.db_name} database is not open"

        query = QSqlQuery(self.con)
        query_str = "SELECT name FROM sqlite_master WHERE "
        query_str += f"type='table' AND name='{table_name}';"
        query.exec(query_str)

        if query.next():
            return True, f"Table {table_name} exists in {self.db_name} database"
        else:
            return False, f"Table {table_name} does not exist in {self.db_name} database"

    # ------------------------------------------------------------------------------------------

    def remove_db(self) -> None:
        """
        If the connection has been terminated, the database object is still persistent.
        This method removed the database object, so it does not get mangled with
        other objects.
        """
        if self.isOpen():
            self.close_db()
        QSqlDatabase.removeDatabase(self.connectionName())


# ==========================================================================================
# ==========================================================================================


class ToDoDatabase(SQLiteManager):
    """
    Class to handle database manager for Todo application

    :param db_name: The database name
    """

    def __init__(self, db_name: str):
        super().__init__(db_name)

    # ------------------------------------------------------------------------------------------

    def create_tasks_table(self) -> tuple[bool, str]:
        """
        Method to create a task table if it does not already exist

        :return: A tuple containing a boolean and a string. A boolean of
                  True indicates the operation was successful, and the string
                  contains a description of the result
        """
        # Check to see if table already exists
        success, msg = self.table_exists("tasks")
        if success:
            return success, msg

        # Create table if it does not already exist
        table_name = "tasks"
        cols = ["task_id", "task", "start_date", "end_date"]
        types = ["INTEGER PRIMARY KEY", "TEXT NOT NULL", "DATE", "DATE"]
        success, msg = self.create_table(table_name, cols, types)
        return success, msg

    # ------------------------------------------------------------------------------------------

    def insert_task(self, task) -> tuple[bool, str, int]:
        """
        Method to insert a task to the tasks table of a database

        :param task: A todo list task represented as a character string
        :return: A tuple containing a boolean and a string. A boolean of
                  True indicates the operation was successful, and the string
                  contains a description of the result
        """
        start_date = datetime.now().strftime("%Y-%m-%d")
        query = QSqlQuery(self.con)
        query.prepare("INSERT INTO tasks (task, start_date) VALUES (?, ?);")
        query.addBindValue(task)
        query.addBindValue(start_date)
        success = query.exec()
        if success:
            task_id = query.lastInsertId()
            return True, f"Task '{task}' successfully added to tasks.", task_id
        else:
            return False, query.lastError().text(), 0

    # ------------------------------------------------------------------------------------------

    def complete_task(self, task_id: int) -> tuple[bool, str]:
        """
        Method to complete task by entering its end date

        :param task_id: The interger id associated with a task
        :return: A tuple containing a boolean and a string. A boolean of
                  True indicates the operation was successful, and the string
                  contains a description of the result
        """
        end_date = datetime.now().strftime("%Y-%m-%d")
        query = "UPDATE tasks SET end_date=? WHERE task_id=?;"
        params = (end_date, task_id)
        success, _, message = self.db_query(query, params)
        if success:
            return True, f"Task id {task_id} successfully completed."
        else:
            return False, message

    # ------------------------------------------------------------------------------------------

    def delete_task(self, task_id: int) -> tuple[bool, str]:
        """
        Method to delete a task from the tasks table of a database.

        :param task_id: The integer id associated with a task
        :return: A tuple containing a boolean and a string. A boolean of
                  True indicates the operation was successful, and the string
                  contains a description of the result
        """
        query = "DELETE FROM tasks WHERE task_id=?;"
        params = (task_id,)
        success, _, message = self.db_query(query, params)
        if success:
            return True, f"Task id {task_id} successfully deleted."
        else:
            return False, message

    # ------------------------------------------------------------------------------------------

    def select_open_tasks(self) -> tuple[bool, pd.DataFrame, str]:
        """
        Method to select all tasks that are still open.

        :param task_id: The integer id associated with a task
        :return: A tuple containing a boolean, a pandas dataframe and a string.
                 A boolean of True indicates the operation was successful, the pandas
                 dataframe contains the results of the query, and the string
                 contains a description of the result
        """
        tasks = []
        query = "SELECT task_id, task FROM tasks WHERE end_date IS NULL"
        success, result, message = self.db_query(query, None)
        if success:
            while result.next():
                tasks.append([result.value(0), result.value(1)])  # get the task text
            df = pd.DataFrame(tasks, columns=["task_id", "task"])
            return True, df, message
        else:
            return False, pd.DataFrame(), message

    # ------------------------------------------------------------------------------------------

    def select_closed_tasks(
        self, time_frame: str, date=datetime.now().strftime("%Y-%m-%d")
    ) -> tuple[bool, pd.DataFrame, str]:
        """
        Method to select all tasks that have been closed within a certain time frame
        of a given date

        :param time_frame: 'DAY', 'WEEEK', 'MONTH', 'YEAR', 'ALL'
        :param date: A datetime object in the format strftime("%Y-%m-%d")
        :return: A tuple containing a boolean, a pandas dataframe and a string.
                 A boolean of True indicates the operation was successful, the pandas
                 dataframe contains the results of the query, and the string
                 contains a description of the result
        """
        time_frame = time_frame.upper()
        expected = ["DAY", "WEEK", "MONTH", "YEAR", "ALL"]
        if time_frame not in expected:
            return False, pd.DataFrame(), "time_frame not correctly formatted"

        if time_frame == "DAY":
            query = "SELECT task_id, task FROM tasks WHERE end_date=?;"
            params = (date,)
        elif time_frame == "WEEK":
            date = datetime.strptime(date, "%Y-%m-%d")
            start_date = (date - timedelta(days=date.weekday())).strftime("%Y-%m-%d")
            query = "SELECT task_id, task FROM tasks WHERE end_date BETWEEN "
            query += "? AND ?;"
            params = (start_date, date.strftime("%Y-%m-%d"))
        elif time_frame == "MONTH":
            date = datetime.strptime(date, "%Y-%m-%d")
            start_date = date.replace(day=1).strftime("%Y-%m-%d")
            query = "SELECT task_id, task FROM tasks WHERE end_date BETWEEN "
            query += "? AND ?;"
            params = (start_date, date.strftime("%Y-%m-%d"))
        elif time_frame == "YEAR":
            date = datetime.strptime(date, "%Y-%m-%d")
            start_date = date.replace(day=1, month=1).strftime("%Y-%m-%d")
            query = "SELECT task_id, task FROM tasks WHERE end_date BETWEEN "
            query += "? AND ?;"
            params = (start_date, date.strftime("%Y-%m-%d"))
        else:
            query = "SELECT task_id, task FROM tasks WHERE end_date IS NOT NULL;"
            params = None

        success, result, message = self.db_query(query, params)
        tasks = []
        msg = f"Successfully retrieved tasks for time_frame: {time_frame}."
        if success:
            while result.next():
                tasks.append([result.value(0), result.value(1)])  # get the task text
            df = pd.DataFrame(tasks, columns=["task_id", "task"])
            return True, df, msg
        else:
            return False, pd.DataFrame(), message


# ==========================================================================================
# ==========================================================================================
# eof
