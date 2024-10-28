import datetime

from db.db_stuff import Task

import pytest
from peewee import IntegrityError


def test_task_create_ok(db_connection):
    assert Task.select().count() == 0
    task = Task.create(title="test", task_date=None)
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
