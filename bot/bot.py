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


@bot.message_handler(commands=["add_tasks"])
async def add_tasks(message):
    if not await check_user(bot, message, config["MY_TG_USERNAME"]):
        return
    try:
        parsed_dict = parse_args(message.text)
        for task_title in parsed_dict["titles"]:
            task = Task.create(title=task_title.strip().lower())
            await bot.reply_to(
                message,
                f"""Created task with id: {task.id}, title: {task.title},
                status: {task.status} task_date: {task.task_date.date()}""",
            )
    except Exception as exc:
        await bot.reply_to(
            message,
            f"Error during creating tasks: {exc}",
        )


@bot.message_handler(commands=["get_tasks"])
async def get_tasks(message):
    if not await check_user(bot, message, config["MY_TG_USERNAME"]):
        return

    parsed_dict = parse_args(message.text)

    if parsed_dict:
        date_str = parsed_dict["dates"][0]
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
        query = Task.select().where(Task.task_date == requested_date)
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
        if tasks:
            await bot.reply_to(
                message,
                f"""Here is your tasks for {requested_date.strftime(DATE_FMT)}:\n\n{" \n".join(tasks)},\n\n stats: {json.dumps(stats, indent=2)}""",
            )
        else:
            await bot.reply_to(
                message,
                f"""Sorry, there is no tasks for {requested_date.strftime(DATE_FMT)}""",
            )


c1 = types.BotCommand(command="start", description="Start the Bot")
c2 = types.BotCommand(command="add_tasks", description="Add some Tasks")
c3 = types.BotCommand(
    command="get_tasks", description="Get all tasks for today"
)


asyncio.run(bot.set_my_commands([c1, c2, c3]))
asyncio.run(bot.polling())
