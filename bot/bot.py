import asyncio
from datetime import datetime
from collections import defaultdict

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
            today_date = datetime.strptime(date_str, "%d.%m.%Y")
        except ValueError as err:
            await bot.reply_to(
                message,
                f"Error converting date {date_str} to datetime: {err}",
            )
            return
    else:
        today_date = datetime.today().date()

    try:
        query = Task.select().where(Task.created_at == today_date)
        stats = defaultdict(int)
        tasks = []
        for task in query:
            tasks.append(task)
            stats[task.status] += 1
    except Exception as exc:
        await bot.reply_to(
            message,
            f"Error during getting tasks: {exc}",
        )
    else:
        await bot.reply_to(
            message,
            f"Here is your tasks for {today_date}: {tasks}, stats: {stats}",
        )


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
async def echo_message(message):
    if not await check_user(bot, message, config["MY_TG_USERNAME"]):
        return
    await bot.reply_to(message, message.text)


c1 = types.BotCommand(command="start", description="Start the Bot")
c2 = types.BotCommand(command="add_task", description="Add the Task")
c3 = types.BotCommand(
    command="get_tasks", description="Get all tasks for today"
)


asyncio.run(bot.set_my_commands([c1, c2, c3]))
asyncio.run(bot.polling())
