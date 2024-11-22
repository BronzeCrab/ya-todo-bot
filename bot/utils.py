from datetime import datetime, timedelta

from dotenv import dotenv_values

from bot.task_dc import TaskItem

config = dotenv_values(".env")

DATE_FMT = config["DATE_FMT"]


async def check_user(bot, message, username: str) -> bool:
    if message.chat.username != config["MY_TG_USERNAME"]:
        await bot.reply_to(message, "sorry, this bot is not public")
        return False
    return True


def parse_arg(
    parsed: dict, command_str: str, j: int, arg: str, init_arg: str = None
) -> int:
    tmp_str = ""
    while j < len(command_str) and command_str[j] not in ("-", "--"):
        tmp_str += command_str[j].strip()
        j += 1
    parsed[arg] = tmp_str.split(";")
    parsed[arg] = [x for x in parsed[arg] if x]

    if len(parsed[arg]) == 0:
        raise Exception(
            f"ERROR: no proper values for {init_arg if init_arg else arg} arg in command {command_str}"
        )

    return j


def parse_args(command_str: str) -> dict:
    parsed_dict = dict()
    i = 0
    possible_args = ("-t", "-d", "-s", "-i")
    possible_verbose_args = ("--titles", "--dates", "--statuses", "--indexes")
    while i < len(command_str):
        if command_str[i : i + len("-t")].lower() in possible_args:
            init_arg = command_str[i : i + len("-t")].lower()
            j = i + len("-t")
            arg = possible_verbose_args[possible_args.index(init_arg)][2:]
            j = parse_arg(parsed_dict, command_str, j, arg, init_arg)
            i = j
        elif (
            command_str[i : i + len(possible_verbose_args[0])].lower()
            == possible_verbose_args[0]
        ):
            j = i + len(possible_verbose_args[0])
            j = parse_arg(
                parsed_dict, command_str, j, possible_verbose_args[0][2:]
            )
            i = j
        elif (
            command_str[i : i + len(possible_verbose_args[1])].lower()
            == possible_verbose_args[1]
        ):
            j = i + len(possible_verbose_args[1])
            j = parse_arg(
                parsed_dict, command_str, j, possible_verbose_args[1][2:]
            )
            i = j
        elif (
            command_str[i : i + len(possible_verbose_args[2])].lower()
            == possible_verbose_args[2]
        ):
            j = i + len(possible_verbose_args[2])
            j = parse_arg(
                parsed_dict, command_str, j, possible_verbose_args[2][2:]
            )
            i = j
        elif (
            command_str[i : i + len(possible_verbose_args[3])].lower()
            == possible_verbose_args[3]
        ):
            j = i + len(possible_verbose_args[3])
            j = parse_arg(
                parsed_dict, command_str, j, possible_verbose_args[3][2:]
            )
            i = j
        else:
            i += 1

    # /add_tasks command should has some titles:
    if command_str.startswith("/add_tasks") and "titles" not in parsed_dict:
        raise Exception(
            f"ERROR: no '-t' or '--titles' arg in command {command_str}"
        )

    # all command except /get_tasks should have some args:
    elif not command_str.startswith("/get_tasks") and not parsed_dict:
        raise Exception(
            f"ERROR: no valid command args in command {command_str}"
        )

    return parsed_dict


def convert_str_date_to_datetime(possible_date_str):
    if type(
        possible_date_str
    ) is str and possible_date_str.strip().lower().startswith("tod"):
        return datetime.today().date()
    elif type(
        possible_date_str
    ) is str and possible_date_str.strip().lower().startswith("tom"):
        return datetime.today().date() + timedelta(days=1)
    elif type(
        possible_date_str
    ) is str and possible_date_str.strip().lower() in (
        "nd",
        "no_date",
        "nodate",
        "ndate",
        "n_date",
    ):
        return "nodate"
    elif type(possible_date_str) is str:
        return datetime.strptime(possible_date_str, DATE_FMT)

    return possible_date_str


def check_status(possible_status) -> list[str]:
    if possible_status:
        allowed_statuses = config["POSSIBLE_STATUSES"].split(";")
        allowed_statuses = [st.lower().strip() for st in allowed_statuses]

        if "+" in possible_status:
            possible_statuses = possible_status.split("+")
        else:
            possible_statuses = [possible_status]

        for p_s in possible_statuses:
            if p_s.strip().lower() not in allowed_statuses:
                raise Exception(
                    f"ERROR: status {p_s} is not allowed, allowed: {allowed_statuses}"
                )
        return possible_statuses


def get_current_item(
    alist: list,
    ind: int,
    is_dates=False,
    is_statuses=False,
):
    if ind < len(alist):
        item = alist[ind]
    elif len(alist) == 1:
        item = alist[0]
    else:
        item = None

    if is_dates:
        return convert_str_date_to_datetime(item)
    elif is_statuses:
        return check_status(item)
    return item


def parse_task_items(parsed_dict: dict) -> list[TaskItem]:
    titles, task_dates, indexes, statuses = [], [], [], []
    if "titles" in parsed_dict:
        titles = parsed_dict["titles"]
    if "dates" in parsed_dict:
        task_dates = parsed_dict["dates"]
    if "indexes" in parsed_dict:
        indexes = parsed_dict["indexes"]
    if "statuses" in parsed_dict:
        statuses = parsed_dict["statuses"]

    task_items: list[TaskItem] = []
    i = 0
    while not (
        i >= len(titles)
        and i >= len(task_dates)
        and i >= len(indexes)
        and i >= len(statuses)
    ):
        title = get_current_item(titles, i)
        task_date = get_current_item(task_dates, i, is_dates=True)
        index = get_current_item(indexes, i)
        status = get_current_item(statuses, i, is_statuses=True)

        task_item = TaskItem(
            title=title,
            index=index,
            status=status,
            task_date=task_date,
        )
        task_items.append(task_item)

        i += 1

    return task_items
