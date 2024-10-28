from dataclasses import dataclass
from datetime import datetime


@dataclass
class TaskItem:
    """Class for keeping track of Task before creation in db."""

    title: str
    index: int = None
    status: str = "todo"
    task_date: str = None