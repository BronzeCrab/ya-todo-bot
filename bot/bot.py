import asyncio
from datetime import datetime
from collections import defaultdict
import json

from telebot import types
from telebot.async_telebot import AsyncTeleBot

from bot.utils import check_user, config, parse_args
from db.db_stuff import Task

bot = AsyncTeleBot(config["BOT_API_KEY"])
DATE_FMT = "%d.%m.%Y"


# Handle '/start' and '/help'
@bot.message_handler(commands=["help", "start"])
async def send_welcome(message):
    if not await check_user(bot, message, config["MY_TG_USERNAME"]):
        return
    text = "Hi, it's yet another todo app, but as telegram bot."
    await bot.reply_to(message, text)


# todo: remake this func to receive multiple tasks
@bot.message_handler(commands=["add_tasks"])
async def add_tasks(message):
    if not await check_user(bot, message, config["MY_TG_USERNAME"]):
        return
    try:
        splited = message.text.split(" ")
        task_title = " ".join(splited[1:])
        task = Task.create(title=task_title.strip())
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


@bot.message_handler(commands=["get_tasks"])
async def get_tasks(message):
    if not await check_user(bot, message, config["MY_TG_USERNAME"]):
        return

    splited = message.text.split(" ")
    date_str = " ".join(splited[1:]).strip().lower()
    if date_str:
        try:
            requested_date = datetime.strptime(date_str, DATE_FMT)
        except ValueError as err:
            await bot.reply_to(
                message,
                f"Error converting date {date_str} to datetime: {err}",
            )
            return
    else:
        requested_date = datetime.today().date()

    try:
        query = Task.select().where(Task.created_at == requested_date)
        stats = defaultdict(int)
        tasks = []
        for task in query:
            tasks.append(str(task))
            stats[task.status] += 1
    except Exception as exc:
        await bot.reply_to(
            message,
            f"Error during getting tasks: {exc}",
        )
    else:
        await bot.reply_to(
            message,
            f"""Here is your tasks for {requested_date.strftime(DATE_FMT)}:\n\n{" \n".join(tasks)},\n\n stats: {json.dumps(stats, indent=2)}""",
        )


c1 = types.BotCommand(command="start", description="Start the Bot")
c2 = types.BotCommand(command="add_tasks", description="Add some Tasks")
c3 = types.BotCommand(
    command="get_tasks", description="Get all tasks for today"
)


asyncio.run(bot.set_my_commands([c1, c2, c3]))
asyncio.run(bot.polling())
