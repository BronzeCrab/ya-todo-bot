import datetime

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


def test_add_tasks_for_today():
    command_str = "/add_tasks -d today -t title1;title2 -s todo;done"
    parsed_dict = parse_args(command_str)
    assert parsed_dict == {
        "dates": ["today"],
        "titles": ["title1", "title2"],
        "statuses": ["todo", "done"],
    }


def test_add_tasks_no_args():
    command_str = "/add_tasks"
    with pytest.raises(Exception) as exc:
        parse_args(command_str)
    assert (
        str(exc.value)
        == f"ERROR: no '-t' or '--titles' arg in command {command_str}"
    )

    command_str = "/add_tasks -i 1;2"
    with pytest.raises(Exception) as exc:
        parse_args(command_str)
    assert (
        str(exc.value)
        == f"ERROR: no '-t' or '--titles' arg in command {command_str}"
    )


def test_edit_tasks_no_args():
    command_str = "/edit_tasks"
    with pytest.raises(Exception) as exc:
        parse_args(command_str)
    assert (
        str(exc.value)
        == f"ERROR: no valid command args in command {command_str}"
    )


def test_get_tasks_ok():
    parsed_dict = parse_args("/get_tasks")
    assert not parsed_dict

    parsed_dict = parse_args("/get_tasks -d 11.07.1989")
    assert parsed_dict == {"dates": ["11.07.1989"]}


def test_get_tasks_plus_statuses():
    parsed_dict = parse_args("/get_tasks -d 11.07.1989 -s todo+done")
    assert parsed_dict == {"dates": ["11.07.1989"], "statuses": ["todo+done"]}


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
    status = get_current_item(statuses, ind, is_statuses=True)
    assert status == [statuses[ind]]

    statuses = ["todo", "doing", "done"]
    ind = len(statuses)
    status = get_current_item(statuses, ind, is_statuses=True)
    assert status is None

    statuses = ["todo"]
    ind = len(statuses) + 1
    status = get_current_item(statuses, ind)
    assert status == statuses[0]

    statuses = ["todo"]
    ind = 0
    status = get_current_item(statuses, ind)
    assert status == statuses[0]

    dates = ["11.07.1989", " toDay   "]
    ind = 0
    some_date = get_current_item(dates, ind, is_dates=True)
    assert isinstance(some_date, datetime.date)

    ind = 1
    some_date = get_current_item(dates, ind, is_dates=True)
    assert some_date != dates[ind]
    assert isinstance(some_date, datetime.date)


def test_get_current_item_tomorrow():
    dates = ["11.07.1989", " toDay   ", "tomorrow"]
    ind = 2
    some_date = get_current_item(dates, ind, is_dates=True)
    assert some_date != dates[ind]
    assert isinstance(some_date, datetime.date)
    assert some_date > datetime.datetime.today().date()


def test_get_current_item_status_exception():
    statuses = ["todo", "doing42", "done"]
    ind = 1
    with pytest.raises(Exception) as exc:
        get_current_item(statuses, ind, is_statuses=True)
    assert str(exc.value).startswith(
        f"ERROR: status {statuses[ind]} is not allowed"
    )


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
    assert task_items[0].task_date is not None

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

    adate = datetime.datetime.strptime(some_dates[0], "%d.%m.%Y")
    assert task_items[0].title == some_titles[0]
    assert task_items[0].index is None
    assert task_items[0].status == [some_statuses[0]]
    assert task_items[0].task_date == adate

    assert task_items[1].title == some_titles[1]
    assert task_items[1].index is None
    assert task_items[1].status == [some_statuses[1]]
    assert task_items[1].task_date == adate

    assert task_items[2].title is None
    assert task_items[2].index is None
    assert task_items[2].status == [some_statuses[2]]
    assert task_items[1].task_date == adate
