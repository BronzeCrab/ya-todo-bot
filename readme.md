## What is it:

It's yet another todo app, but as telegram bot.

## How to run it:

Install dependencies:

```sh
pip install -r requirements.txt
```

Copy `.env_example` file:

```sh
cp .env_example .env
```

Populate `.env` file with your `MY_TG_USERNAME` and your `BOT_API_KEY`,
also, you can specify `POSSIBLE_STATUSES` divided by `;` and your `DATE_FMT` as you want, then:

```sh
python -m bot.bot
```

## How to use this bot:

This bot has several commands: `/add_tasks`, `/get_tasks`, `/edit_tasks`, `/delete_tasks`,
`/copy_tasks`, `/move_tasks`

### How to create tasks (`/add_tasks` command):

Create two tasks with titles `title1` and `title2` for current date:

```sh
/add_tasks -t title1;title2
```
Or, you can do exactly the same command with another arg name:

```sh
/add_tasks --titles title1;title2
```

Create two tasks with titles `title1` and `title2` for specific date:

```sh
/add_tasks -t title1;title2 -d 27.10.2024
```

Create two tasks with titles `title1` and `title2` for specific date
with statuses `todo` and `done` respectively:

```sh
/add_tasks -t title1;title2 -d 27.10.2024 -s todo;done
```

Create two tasks with titles `title1` and `title2` for today date
with status `todo`:

```sh
/add_tasks -t title1;title2 -d today -s todo
```

### How to get tasks (`/get_tasks` command):

Get all tasks for today:

```sh
/get_tasks -d today
```

Get all tasks for today with `todo` status:

```sh
/get_tasks -s todo -d today
```

Get all tasks for specific date with `todo` status:

```sh
/get_tasks -d 27.10.2024 -s todo
```

Get all tasks for specific dates with `todo` and `done` statuses respectively (
i.e. only `todo` tasks from first date, plus only `done` from second date):

```sh
/get_tasks -d 27.10.2024;28.10.2024 -s todo;done
```

Get all tasks for specific dates with `todo` and `done` statuses (
i.e. all tasks with both statues from two dates):

```sh
/get_tasks -d 27.10.2024;28.10.2024 -s todo+done
```

## How to run tests:

```sh
python -m pytest
```
