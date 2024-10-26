import datetime

from peewee import Model, SqliteDatabase, CharField, DateField, Check, SQL

db = SqliteDatabase("todo.db")


class Task(Model):
    title = CharField(
        constraints=[
            Check("length(title) > 0"),
        ]
    )
    status = CharField(default="todo")
    created_at = DateField(
        default=datetime.datetime.now,
    )

    class Meta:
        database = db
        constraints = [SQL("UNIQUE (title, created_at)")]


db.connect()
db.create_tables([Task])
