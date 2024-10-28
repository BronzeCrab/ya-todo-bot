from datetime import datetime

import pytest

from db.db_stuff import Task, SqliteDatabase


@pytest.fixture(scope="function")
def db_connection():
    test_db = SqliteDatabase("test_todos.db")
    test_db.connect()
    test_db.create_tables([Task])
    yield test_db
    q = Task.delete()
    q.execute()


@pytest.fixture(scope="function")
def created_task():
    assert Task.select().count() == 0
    task = Task.create(title="test", task_date=datetime.today().date())
    assert Task.select().count() == 1
    yield task
