import discord
from discord.ext.commands import Bot
from discord.ext.commands.help import MinimalHelpCommand
from vdbot.config import config
from PyDictionary import PyDictionary
from discord import Embed, activity

from datetime import datetime

from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

class Statistics:
    def __init__(self):
        self.command_count = 0
        self.msgs_parsed = 0
        self.start_time = datetime.now()

    def get_uptime(self):
        td = datetime.now() - self.start_time
        days = td.days
        hours, remainder = divmod(td.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return days, hours, minutes, seconds

def create_bot():
    dictionary = PyDictionary()
    bot = Bot("!")
    console = Console(width=80)
    stats = Statistics()
    return bot, dictionary, console, stats

bot, dictionary, console, stats = create_bot()

from .cogs import *

from .event_listeners import *

async def on_ready():
    activity = discord.Activity(name="How To: Mod Valheim Like A Pro", type=discord.ActivityType.watching)
    await bot.change_presence(status=discord.Status.online, activity=activity)

bot.add_listener(on_ready)

@bot.before_invoke
async def command_logger(ctx):
    stats.command_count += 1
    console.print(Panel('[bold green]Called Command'), justify='center')
    console.print(Panel('[bold green]Command: [/bold green]' + ctx.command.name + '\n[bold green] Possible Aliases: [/bold green]' + str(ctx.command.aliases)), justify='center')


def run_bot():
    try:
        bot.run(config.token, bot=True)
    except KeyboardInterrupt:
        bot.close()
        exit()