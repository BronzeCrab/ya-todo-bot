## What is it:

It's yet another todo app, but as telegram bot.

## How to run it:

Install dependencies:

```
pip install -r requirements.txt
```

Copy .env_example:

```sh
cp .env_example .env
```

Populate `.env` with your `MY_TG_USERNAME` and your `BOT_API_KEY`, then:

```sh
python -m bot.bot
```

## How to run tests:

```sh
python -m pytest
```
