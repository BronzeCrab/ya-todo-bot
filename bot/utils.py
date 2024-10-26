from dotenv import dotenv_values


config = dotenv_values(".env")


async def check_user(bot, message, username: str) -> bool:
    if message.chat.username != config["MY_TG_USERNAME"]:
        await bot.reply_to(message, "sorry, this bot is not public")
        return False
    return True


def parse_titles(parsed: dict, command_str: str, j: int) -> None:
    tmp_str = ""
    while j < len(command_str):
        tmp_str += command_str[j].strip()
        j += 1
    parsed["titles"] = tmp_str.split(";")


def parse_args(command_str: str) -> dict:
    parsed_dict = dict()
    i = 0
    while i < len(command_str):
        if "titles" not in parsed_dict:
            if command_str[i : i + len("-t")].lower() == "-t":
                j = i + len("-t")
                parse_titles(parsed_dict, command_str, j)
            elif command_str[i : i + len("--titles")].lower() == "--titles":
                j = i + len("--titles")
                parse_titles(parsed_dict, command_str, j)
        i += 1

    return parsed_dict
