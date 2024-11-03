import datetime

from db.db_stuff import Task, check_if_task_exitsts

import pytest
from peewee import IntegrityError


def test_task_create_ok(db_connection):
    assert Task.select().count() == 0
    task = Task.create(title="test", task_date=None)
    assert Task.select().count() == 1
    assert task.title == "test"
    assert task.task_date is None
    assert task.status == "todo"


def test_task_create_2_tasks_with_None_date_same_title(db_connection):
    assert Task.select().count() == 0
    task = Task.create(title="test", task_date=None)
    assert Task.select().count() == 1
    assert task.title == "test"
    assert task.task_date is None
    assert task.status == "todo"

    task = Task.create(title="test", task_date=None)
    assert Task.select().count() == 2


def test_task_create_date_should_be_None(db_connection):
    assert Task.select().count() == 0
    task = Task.create(title="test")
    assert Task.select().count() == 1
    assert task.title == "test"
    assert task.task_date is None
    assert task.status == "todo"


def test_task_create_with_not_null_date(db_connection):
    assert Task.select().count() == 0
    task = Task.create(
        title="test",
        task_date=datetime.datetime.today().date(),
    )
    assert Task.select().count() == 1
    assert task.title == "test"
    assert isinstance(task.task_date, datetime.date)
    assert task.status == "todo"


def test_task_create_with_str_date(db_connection):
    assert Task.select().count() == 0
    str_date = "11.07.1989"
    task = Task.create(
        title="test",
        task_date=str_date,
    )
    assert Task.select().where(Task.title == str_date).count() == 0
    assert task.title == "test"
    assert isinstance(task.task_date, str)
    assert task.status == "todo"


def test_task_create_no_title(db_connection):
    assert Task.select().count() == 0
    with pytest.raises(IntegrityError) as err:
        task = Task.create()
    assert str(err.value) == "NOT NULL constraint failed: task.title"
    assert Task.select().count() == 0


def test_task_create_duplicate_err(db_connection, created_task):
    assert Task.select().count() == 1
    with pytest.raises(IntegrityError) as err:
        task = Task.create(
            title=created_task.title, task_date=created_task.task_date
        )
    assert (
        str(err.value) == "UNIQUE constraint failed: task.title, task.task_date"
    )
    assert Task.select().count() == 1


def test_query_task_by_id(db_connection, created_task):
    assert Task.select().count() == 1

    task = Task.select().where(Task.id == created_task.id).get()

    assert task.id == created_task.id
    assert task.title == created_task.title


def test_check_if_task_exitsts(db_connection, created_task):
    assert check_if_task_exitsts(created_task.title) is True
    assert check_if_task_exitsts("afoobar42") is False

    upper_title = created_task.title.upper()
    assert check_if_task_exitsts(upper_title) is True
