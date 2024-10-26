from dotenv import dotenv_values


config = dotenv_values(".env")


async def check_user(bot, message, username: str) -> bool:
    if message.chat.username != config["MY_TG_USERNAME"]:
        await bot.reply_to(message, "sorry, this bot is not public")
        return False
    return True
