from dotenv import dotenv_values


config = dotenv_values(".env")


async def check_user(bot, message, username: str) -> bool:
    if message.chat.username != config["MY_TG_USERNAME"]:
        await bot.reply_to(message, "sorry, this bot is not public")
        return False
    return True


def parse_arg(parsed: dict, command_str: str, j: int, arg: str) -> int:
    tmp_str = ""
    while j < len(command_str) and command_str[j] not in ("-", "--"):
        tmp_str += command_str[j].strip()
        j += 1
    parsed[arg] = tmp_str.split(";")
    return j


def parse_args(command_str: str) -> dict:
    parsed_dict = dict()
    i = 0
    possible_args = ("-t", "-d", "-s", "-i")
    possible_verbose_args = ("--titles", "--days", "--statuses", "--indexes")
    while i < len(command_str):
        if command_str[i : i + len("-t")].lower() in possible_args:
            j = i + len("-t")
            arg = possible_verbose_args[
                possible_args.index(command_str[i : i + len("-t")].lower())
            ][2:]
            j = parse_arg(parsed_dict, command_str, j, arg)
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

    return parsed_dict
