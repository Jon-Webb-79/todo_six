# Import necessary packages here
import os

import pytest

from todo_six.database import SQLiteManager

# ==========================================================================================
# ==========================================================================================
# File:    database_test.py
# Date:    June 05, 2023
# Author:  Jonathan A. Webb
# Purpose: This file tests the methods and classes in the database.py file
# Instruction: This code can be run in hte following ways
#              - pytest # runs all functions beginnning with the word test in the
#                         directory
#              - pytest file_name.py # Runs all functions in file_name beginning
#                                      with the word test
#              - pytest file_name.py::test_func_name # Runs only the function
#                                                      titled test_func_name in
#                                                      the file_name.py file
#              - pytest -s # Runs tests and displays when a specific file
#                            has completed testing, and what functions failed.
#                            Also displays print statments
#              - pytest -v # Displays test results on a function by function
#              - pytest -p no:warnings # Runs tests and does not display warning
#                          messages
#              - pytest -s -v -p no:warnings # Displays relevant information and
#                                supports debugging
#              - pytest -s -p no:warnings # Run for record
# ==========================================================================================
# ==========================================================================================
# Insert Code here


@pytest.fixture(scope="module")
def db_manager():
    db_path = "test_db.sqlite"
    # yield the database manager, and ensure the database file is removed after each test
    manager = SQLiteManager(db_path)
    yield manager
    if manager.con.isOpen():
        manager.close_db()
    if os.path.exists(db_path):
        os.remove(db_path)


# ==========================================================================================
# ==========================================================================================


@pytest.mark.sqlitemanager
def test_open_close_db(db_manager):
    assert not db_manager.con.isOpen()
    success, _ = db_manager.open_db()
    assert success
    assert db_manager.con.isOpen()
    success, _ = db_manager.close_db()
    assert success
    assert not db_manager.con.isOpen()


# ------------------------------------------------------------------------------------------


@pytest.mark.sqlitemanager
def test_create_table(db_manager):
    success, _ = db_manager.open_db()
    assert success
    success, _ = db_manager.create_table("test", ["id", "name"], ["INTEGER", "TEXT"])
    assert success
    success, _ = db_manager.close_db()
    assert success


# ------------------------------------------------------------------------------------------


@pytest.mark.sqlitemanager
def test_table_schema(db_manager):
    success, _ = db_manager.open_db()
    assert success
    success, schema, _ = db_manager.table_schema("test")
    assert success
    assert schema == {"id": "INTEGER", "name": "TEXT"}
    success, _ = db_manager.close_db()
    assert success


# ------------------------------------------------------------------------------------------


@pytest.mark.sqlitemanager
def test_db_schema(db_manager):
    success, _ = db_manager.open_db()
    assert success
    success, schema, _ = db_manager.db_schema()
    assert success
    assert schema == {"test": {"id": "INTEGER", "name": "TEXT"}}
    success, _ = db_manager.close_db()
    assert success


# ------------------------------------------------------------------------------------------


@pytest.mark.sqlitemanager
def test_table_exists(db_manager):
    success, _ = db_manager.open_db()
    assert success
    exists, _ = db_manager.table_exists("test")
    assert exists
    exists, _ = db_manager.table_exists("non_existent_table")
    assert not exists
    success, _ = db_manager.close_db()
    assert success


# ------------------------------------------------------------------------------------------


@pytest.mark.sqlitemanager
def test_db_query(db_manager):
    success, _ = db_manager.open_db()
    assert success

    # first, create a table and insert some data
    success, _ = db_manager.create_table("new_test", ["id", "name"], ["INTEGER", "TEXT"])
    assert success

    success, _, _ = db_manager.db_query(
        "INSERT INTO new_test (id, name) VALUES (1, 'Alice')"
    )
    assert success

    # now, run a SELECT query and check the results
    success, results, _ = db_manager.db_query("SELECT * FROM new_test")
    assert success

    results_list = []
    while results.next():
        id = results.value(0)
        name = results.value(1)
        results_list.append((id, name))

    assert results_list == [(1, "Alice")]

    success, _ = db_manager.close_db()
    assert success


# ==========================================================================================
# ==========================================================================================
# eof
