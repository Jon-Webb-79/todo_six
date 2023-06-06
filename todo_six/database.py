# Import necessary packages here
import sys
from typing import Protocol

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


class SQLManager(Protocol):
    def open_db(self) -> tuple[bool, str]:
        """
        Template method for opening an existing database

        :return result: A tuple containing a boolean and a string.  A boolean of
                        True indicates the operation was successful, and the string
                        contains a description of the result
        """
        ...

    # ------------------------------------------------------------------------------------------

    def close_db(self) -> tuple[bool, str]:
        """
        Template method for closing an existing database

        :return result: A tuple containing a boolean and a string.  A boolean of
                        True indicates the operation was successful, and the string
                        contains a description of the result
        """
        ...

    # ------------------------------------------------------------------------------------------

    def db_query(self, query: str) -> tuple[bool, QSqlQuery, str]:
        """
        Template method for quering a database

        :param query: A string query of a database
        :return result: A tuple containing a boolean and a string.  A boolean of
                        True indicates the operation was successful, and the string
                        contains a description of the result
        """
        ...

    # ------------------------------------------------------------------------------------------

    def table_schema(self, table_name: str) -> tuple[bool, dict[str, str], str]:
        """
        Method to return the column names and datatypes for a table

        :param table_name: The name of the table
        :return result: A tuple containing a boolean and a dictionary. A boolean of
                        True indicates the operation was successful, and the dictionary
                        contains the names of each column and the type associated with
                        each column
        """
        ...

    # ------------------------------------------------------------------------------------------

    def table_exists(self, table_name: str) -> tuple[bool, str]:
        """
        Method to check if a table exists in the database

        :param table_name: The name of the table
        :return: True if the table exists, False otherwise
        """
        ...

    # ------------------------------------------------------------------------------------------

    def db_schema(self) -> tuple[bool, dict[str, dict[str, str]], str]:
        """
        Method to return the column names and datatypes for all tables in the database.

        :return result: A tuple containing a boolean and a nested dictionary. A boolean
                        of True indicates the operation was successful, and the nested
                        dictionary contains the names of each table as keys, each
                        containing a dictionary of column names and the type associated
                        with each column. The string is a description of the result.
        """
        ...

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
        """
        ...


# ==========================================================================================
# ==========================================================================================


class SQLiteManager(QSqlDatabase):
    """
    Class to manage generic SQLite functions

    :param db_name: The name and pathlength to the SQLite database
    :param hostname: The hostname for the database, set to None for SQLite
    :param username: The username for database access, set to None for SQLite
    :param pwd: The password associated with the username, set to None for SQLite
    """

    def __init__(
        self, db_name: str, hostname: str = None, username: str = None, pwd: str = None
    ):
        msg = "Hostname, Username, and Password are no required in SQLite\n"
        if hostname is not None or username is not None or pwd is not None:
            sys.stderr.write(msg)
        self.db_name = db_name
        self.con = self.addDatabase("QSQLITE")
        self.con.setDatabaseName(db_name)
        super().__init__()

    # ------------------------------------------------------------------------------------------

    def open_db(self) -> tuple[bool, str]:
        """
        Method to open an existing database.

        :return result: A tuple containing a boolean and a string.  A boolean of
                        True indicates the operation was successful, and the string
                        contains a description of the result
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
        """
        if not self.con.isOpen():
            # Write to stderr for debugging
            sys.stderr.write(f"{self.db_name} database is not open\n")
            return False, f"{self.db_name} database is not open"
        self.con.close()
        return True, f"{self.db_name} database succesfully closed"

    # ------------------------------------------------------------------------------------------

    def db_query(self, query: str) -> tuple[bool, QSqlQuery, str]:
        """
        Method to query a database

        :param query: A string query of a database
        :return result: A tuple containing a boolean, a QSqlQuery object, and a string.
                        The boolean indicates the operation was successful,
                        the QSqlQuery object contains the query results (if any),
                        and the string contains a description of the result.
        """
        if not self.con.isOpen():
            # Write to stderr for debugging
            sys.stderr.write(f"{self.db_name} database is not open\n")
            return False, QSqlQuery(), f"{self.db_name} database is not open"

        q = QSqlQuery(self.con)
        success = q.exec(query)

        if not success:
            error_message = q.lastError().text()
            # Write to stderr for debugging
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


# ==========================================================================================
# ==========================================================================================
# eof
