from bot.utils import parse_args


def test_parse_args_only_titles():
    parsed_dict = parse_args("/add_tasks -t title1;title2;title3")
    assert parsed_dict == {"titles": ["title1", "title2", "title3"]}

    parsed_dict = parse_args("/add_tasks --titles title1;title2;title3")
    assert parsed_dict == {"titles": ["title1", "title2", "title3"]}
