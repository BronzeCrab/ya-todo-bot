import datetime

from peewee import Model, SqliteDatabase, CharField, DateField, Check

db = SqliteDatabase("todo.db")


class Task(Model):
    title = CharField(constraints=[Check("length(title) > 0")])
    status = CharField(default="todo")
    created_at = DateField(default=datetime.datetime.now)

    class Meta:
        database = db


db.connect()
db.create_tables([Task])
