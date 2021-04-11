# Valheim Modding Discord - Böt of Yggdrasil

 A discord bot for helping out in the Valheim Modding Discord

 # Features

 - Welcome Messages
 - HowDoI Module for getting StackOverflow Results
 - PyDictionary Module for getting dictionary definitions
 - Mod index and search from Nexusmods.com and Thunderstore for Valheim Mods
 - Embed module for admins
 - Information modules for easier development needs

 # Getting Started

 ### Requirements:

 **(If not using Docker)**
 - Python 3.6+
 - A Discord Bot Token

**(If using Docker)**
- Docker

### How to Run:

**(Without Docker)**
```
# Installing Modules
pip install -r requirements.txt

# On Windows
env BOT_TOKEN=<dicord_bot_token> python -m vdbot

# On Unix
BOT_TOKEN=<discord_bot_token> python -m vdbot
```

**(With Docker)**
```
# On Windows
env BOT_TOKEN=<dicord_bot_token> docker-compose up --build

# On Unix
export BOT_TOKEN=<discord_bot_token>
make start # Runs in background
make start-logs # Runs with logs
```

# Development

If you want to add a cog/module, add it to `vdbot/cogs/` under it's own file. This file should act as a category. We don't use the normal cog system because there is no need for it. If you add a new command, update the help command inside `vdbot/__init__.py`.

Make a PR and ping me in the discord to get it expedited.

# License

Check LICENSE.md