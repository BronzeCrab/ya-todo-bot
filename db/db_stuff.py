from datetime import datetime

from peewee import Model, SqliteDatabase, CharField, DateField, Check, SQL

db = SqliteDatabase("todos.db")


class Task(Model):
    title = CharField(
        constraints=[
            Check("length(title) > 0"),
        ]
    )
    status = CharField(default="todo")
    task_date = DateField(null=True)

    class Meta:
        database = db
        constraints = [SQL("UNIQUE (title, task_date)")]

    def __str__(self) -> str:
        return f"Task_id: {self.id}, status: {self.status}, title: {self.title} date: {self.task_date}"


def check_if_task_exitsts(title: str) -> bool:
    return Task.select().where(Task.title ** title.strip()).exists()


db.connect()
db.create_tables([Task])
