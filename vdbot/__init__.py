import discord
from discord.ext.commands import Bot
from discord.ext.commands.help import MinimalHelpCommand
from vdbot.config import config
from PyDictionary import PyDictionary
from discord import Embed, activity
from vdbot.modfinder import ModFinder

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
    intents = discord.Intents().all()
    mods = ModFinder()
    dictionary = PyDictionary()
    bot = Bot("!", intents=intents)
    console = Console(width=80)
    stats = Statistics()
    return bot, dictionary, console, stats, mods

bot, dictionary, console, stats, mods = create_bot()
bot.remove_command('help')
from .cogs import *

from .event_listeners import *

async def on_ready():
    activity = discord.Activity(name="Over Yggdrasil | !help", type=discord.ActivityType.watching)
    await bot.change_presence(status=discord.Status.online, activity=activity)

bot.add_listener(on_ready)

@bot.before_invoke
async def command_logger(ctx):
    stats.command_count += 1
    console.print(Panel('[bold green]Called Command'), justify='center')
    console.print(Panel('[bold green]Command: [/bold green]' + ctx.command.name + '\n[bold green] Possible Aliases: [/bold green]' + str(ctx.command.aliases)), justify='center')

@bot.command('help')
async def on_help(ctx):
    async with ctx.channel.typing():
        embed = Embed(title="Help Menu", description="Bot Prefix: !")
        embed.add_field(name="!define <word>", value="Define a word quickly from the dictionary")
        embed.add_field(name="!invite", value="Get the permanent invite link")
        embed.add_field(name="!howdoi <your query>", value="Get a StackOverflow snippet by query")
        embed.add_field(name="!mod <mod title>", value="Find links to mods based on a title")
        embed.add_field(name="!wheretostart", value="Find links to the Valheim Modding Wiki easily")
        embed.add_field(name="!template", value="Get an easy plugin class template to copy from")
        embed.add_field(name="!info", value="Get information about the bot")
    await ctx.reply(embed=embed)

    
def run_bot():
    try:
        bot.run(config.token, bot=True)
    except KeyboardInterrupt:
        bot.close()
        exit()