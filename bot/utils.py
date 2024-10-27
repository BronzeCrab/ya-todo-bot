from dotenv import dotenv_values


config = dotenv_values(".env")


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
    # all command except /get_tasks should have args:
    if not command_str.startswith("/get_tasks") and not parsed_dict:
        raise Exception(
            f"ERROR: no valid command args in command {command_str}"
        )

    # /add_tasks also should has some titles:
    if command_str.startswith("/add_tasks") and "titles" not in parsed_dict:
        raise Exception(
            f"ERROR: no '-t' or '--titles' arg in command {command_str}"
        )

    return parsed_dict
