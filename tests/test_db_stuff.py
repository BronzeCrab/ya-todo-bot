from db.db_stuff import Task, SqliteDatabase

test_db = SqliteDatabase("test_todos.db")
test_db.connect()
test_db.create_tables([Task])


def test_task_create():
    q = Task.delete()
    q.execute()
    assert Task.select().count() == 0
    task = Task.create(title="test", task_date=None)
    assert Task.select().count() == 1
    assert task.title == "test"
    assert task.task_date is None
    assert task.status == "todo"
