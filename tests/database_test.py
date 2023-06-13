# Import necessary packages here
import os
import time
from datetime import datetime

import pytest

from todo_six.database import SQLiteManager, ToDoDatabase

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
    manager = SQLiteManager(db_path)
    yield manager
    if manager.con.isOpen():
        manager.remove_db()  # Here, replace close_db() with remove_db()
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
    success, _ = db_manager.create_table(
        "test", ["table_id", "name"], ["INTEGER", "TEXT"]
    )
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
    assert schema == {"table_id": "INTEGER", "name": "TEXT"}
    success, _ = db_manager.close_db()
    assert success


# ------------------------------------------------------------------------------------------


@pytest.mark.sqlitemanager
def test_db_schema(db_manager):
    success, _ = db_manager.open_db()
    assert success
    success, schema, _ = db_manager.db_schema()
    assert success
    assert schema == {"test": {"table_id": "INTEGER", "name": "TEXT"}}
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

    success, _ = db_manager.create_table("new_test", ["id", "name"], ["INTEGER", "TEXT"])
    assert success

    # note the '?' placeholders in the query
    success, _, _ = db_manager.db_query(
        "INSERT INTO new_test (id, name) VALUES (?, ?)", (1, "Alice")
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
# Test ToDoDatabase class


@pytest.fixture(scope="module")
def tododb_manager():
    db_path = "test.db"
    tododb_manager = ToDoDatabase(db_path)
    tododb_manager.open_db()
    yield tododb_manager
    if tododb_manager.con.isOpen():
        tododb_manager.remove_db()  # Here, replace close_db() with remove_db()
    if os.path.exists(db_path):
        os.remove(db_path)


# ------------------------------------------------------------------------------------------


@pytest.mark.tododatabase
def test_create_tasks_table(tododb_manager):
    success, _ = tododb_manager.create_tasks_table()
    assert success


# ------------------------------------------------------------------------------------------


@pytest.mark.tododatabase
def test_insert_task(tododb_manager):
    success, _, task_id = tododb_manager.insert_task("Test Task1")
    assert task_id == 1
    assert success


# ------------------------------------------------------------------------------------------


@pytest.mark.tododatabase
def test_complete_task(tododb_manager):
    success, _, _ = tododb_manager.insert_task("Test Task2")
    assert success
    task_id = 1  # For simplicity, assume the task_id is 1
    success, _ = tododb_manager.complete_task(task_id)
    assert success


# ------------------------------------------------------------------------------------------


@pytest.mark.tododatabase
def test_delete_task(tododb_manager):
    success, _, _ = tododb_manager.insert_task("Test Task3")
    assert success
    task_id = 1  # For simplicity, assume the task_id is 1
    success, _ = tododb_manager.delete_task(task_id)
    assert success


# ------------------------------------------------------------------------------------------


@pytest.mark.tododatabase
def test_select_open_tasks(tododb_manager):
    success, _, _ = tododb_manager.insert_task("Test Task4")
    assert success
    success, tasks, _ = tododb_manager.select_open_tasks()
    expected = ["Test Task2", "Test Task3", "Test Task4"]
    assert success
    assert set(tasks["task"]) == set(expected)


# ------------------------------------------------------------------------------------------


@pytest.mark.tododatabase
def test_select_closed_tasks(tododb_manager):
    success, _, _ = tododb_manager.insert_task("Test Task5")
    assert success
    task_id = 3  # For simplicity, assume the task_id is 1
    success, _ = tododb_manager.complete_task(task_id)
    assert success
    success, tasks, _ = tododb_manager.select_closed_tasks("ALL")
    expected = ["Test Task3"]
    assert success
    assert set(tasks["task"]) == set(expected)


# ------------------------------------------------------------------------------------------


@pytest.mark.tododatabase
def test_get_oldest_date(tododb_manager):
    # Insert some tasks with specific dates
    tododb_manager.insert_task("Task 1")
    tododb_manager.complete_task(1)  # For simplicity, assume the task_id is 1
    # Delay to make sure tasks have different dates
    time.sleep(1)
    tododb_manager.insert_task("Task 2")
    tododb_manager.complete_task(2)  # For simplicity, assume the task_id is 2
    time.sleep(1)
    tododb_manager.insert_task("Task 3")
    tododb_manager.complete_task(3)  # For simplicity, assume the task_id is 3
    # Get the oldest date
    success, oldest_date, _ = tododb_manager.get_oldest_date()
    assert success
    # Compare with expected date
    expected_oldest_date = datetime.now().strftime("%Y-%m-%d")
    assert oldest_date == expected_oldest_date


# ==========================================================================================
# ==========================================================================================
# eof
