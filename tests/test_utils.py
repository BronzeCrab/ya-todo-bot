import pytest

from bot.utils import parse_args, get_current_item, parse_task_items


def test_parse_args_only_titles():
    parsed_dict = parse_args("/add_tasks -t title1;title2;title3")
    assert parsed_dict == {"titles": ["title1", "title2", "title3"]}

    parsed_dict = parse_args("/add_tasks --titles title1;title2;title3")
    assert parsed_dict == {"titles": ["title1", "title2", "title3"]}


def test_parse_args_edit_tasks():
    parsed_dict = parse_args("/edit_tasks -i 1;2 -t title1;title2")
    assert parsed_dict == {
        "indexes": ["1", "2"],
        "titles": ["title1", "title2"],
    }


def test_add_tasks_no_args():
    command_str = "/add_tasks"
    with pytest.raises(Exception) as exc:
        parse_args(command_str)
    assert (
        str(exc.value)
        == f"ERROR: no valid command args in command {command_str}"
    )

    command_str = "/add_tasks -i 1;2"
    with pytest.raises(Exception) as exc:
        parse_args(command_str)
    assert (
        str(exc.value)
        == f"ERROR: no '-t' or '--titles' arg in command {command_str}"
    )


def test_get_tasks_ok():
    parsed_dict = parse_args("/get_tasks")
    assert not parsed_dict

    parsed_dict = parse_args("/get_tasks -d 11.07.1989")
    assert parsed_dict == {"dates": ["11.07.1989"]}


def test_get_tasks_wrong():
    arg = "-d"
    command_str = f"/get_tasks {arg} ;;"
    with pytest.raises(Exception) as exc:
        parse_args(command_str)
    assert (
        str(exc.value)
        == f"ERROR: no proper values for {arg} arg in command {command_str}"
    )


def test_get_current_item():
    statuses = ["todo", "doing", "done"]
    ind = 0
    status = get_current_item(statuses, ind)
    assert status == statuses[ind]

    statuses = ["todo", "doing", "done"]
    ind = len(statuses)
    status = get_current_item(statuses, ind)
    assert status is None

    statuses = ["todo"]
    ind = len(statuses) + 1
    status = get_current_item(statuses, ind)
    assert status == statuses[0]

    statuses = ["todo"]
    ind = 0
    status = get_current_item(statuses, ind)
    assert status == statuses[0]


def test_parse_task_items():
    parsed_dict = {}
    task_items = parse_task_items(parsed_dict)
    assert len(task_items) == 0

    some_title = "title1"
    parsed_dict = {"titles": [some_title]}
    task_items = parse_task_items(parsed_dict)
    assert len(task_items) == 1
    assert task_items[0].title == some_title
    assert task_items[0].index is None
    assert task_items[0].status is None
    assert task_items[0].task_date is None

    some_titles = ["title1", "title2"]
    some_dates = ["27.10.2024"]
    some_statuses = ["todo", "doing", "done"]
    parsed_dict = {
        "titles": some_titles,
        "dates": some_dates,
        "statuses": some_statuses,
    }
    task_items = parse_task_items(parsed_dict)
    assert len(task_items) == 3

    assert task_items[0].title == some_titles[0]
    assert task_items[0].index is None
    assert task_items[0].status == some_statuses[0]
    assert task_items[0].task_date == some_dates[0]

    assert task_items[1].title == some_titles[1]
    assert task_items[1].index is None
    assert task_items[1].status == some_statuses[1]
    assert task_items[1].task_date == some_dates[0]

    assert task_items[2].title is None
    assert task_items[2].index is None
    assert task_items[2].status == some_statuses[2]
    assert task_items[1].task_date == some_dates[0]
