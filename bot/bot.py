import asyncio

from telebot import types
from telebot.async_telebot import AsyncTeleBot

from bot.utils import check_user, config
from db.db_stuff import Task

bot = AsyncTeleBot(config["BOT_API_KEY"])


# Handle '/start' and '/help'
@bot.message_handler(commands=["help", "start"])
async def send_welcome(message):
    if not await check_user(bot, message, config["MY_TG_USERNAME"]):
        return
    text = "Hi, I am EchoBot.\nJust write me something and I will repeat it!"
    await bot.reply_to(message, text)


@bot.message_handler(commands=["add_task"])
async def add_task(message):
    if not await check_user(bot, message, config["MY_TG_USERNAME"]):
        return
    try:
        splited = message.text.split(" ")
        task_title = " ".join(splited[1:])
        task = Task.create(title=task_title)
    except Exception as exc:
        await bot.reply_to(
            message,
            f"Error during creating the task: {exc}",
        )
    else:
        await bot.reply_to(
            message,
            f"""Created task with id: {task.id}, title: {task.title},
            status: {task.status} created_at: {task.created_at.date()}""",
        )


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
async def echo_message(message):
    if not await check_user(bot, message, config["MY_TG_USERNAME"]):
        return
    await bot.reply_to(message, message.text)


c1 = types.BotCommand(command="start", description="Start the Bot")
c2 = types.BotCommand(command="help", description="Click for Help")
c3 = types.BotCommand(command="add_task", description="Add the Task")

asyncio.run(bot.set_my_commands([c1, c2, c3]))
asyncio.run(bot.polling())
