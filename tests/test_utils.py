import pytest

from bot.utils import parse_args


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


def test_parse_args_no_args():
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
