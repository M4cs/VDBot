import discord
from discord.ext.commands import Bot
from discord.ext.commands.help import MinimalHelpCommand
from vdbot.config import config
from PyDictionary import PyDictionary
from discord import Embed, activity
from vdbot.modfinder import ModFinder
from vdbot.db import db
from datetime import datetime
from fuzzywuzzy import process

from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown


class CodeIndexer():
    def __init__(self):
        self.class_names = []
        self.method_names = []
        self.field_names = []
        for clss in db.class_index.find():
            self.class_names.append(clss['name'])
            for meth in clss['methods']:
                self.method_names.append(meth['name'])
            for field in clss['fields']:
                self.field_names.append(field['name'])
    
    def find_class(self, class_name: str):
        if class_name in self.class_names:
            clss = db.class_index.find_one({"name": class_name})
            return True, clss
        else:
            results = process.extract(class_name, self.class_names, limit=3)
            classes = []
            for res in results:
                classes.append(res[0])
            return False, classes

    def find_field(self, field_name: str):
        field_class = None
        if '.' in field_name:
            field_class = field_name.split('.')[0]
            field_name = field_name.split('.')[1]
        if field_name in self.field_names:
            if field_class:
                field = db.class_index.find({"name": field_class, "fields.name": { "$in": [field_name]}})
            else:
                field = db.class_index.find({"fields.name": { "$in": [field_name]}})
            if field:
                return True, field
        else:
            results = process.extract(field_name, self.field_names, limit=3)
            fields = []
            for res in results:
                field = db.class_index.find({"fields.name": { "$in": [res[0]]}})
                fields.append(field)
            return False, fields

    def find_method(self, method_name: str):
        method_class = None
        if '.' in method_name:
            method_class = method_name.split('.')[0]
            method_name = method_name.split('.')[1]
        if method_name in self.method_names:
            if method_class:
                mth = db.class_index.find({"name": method_class, "methods.name": { "$in": [method_name]}})
            else:
                mth = db.class_index.find({"methods.name": { "$in": [method_name]}})
            if mth:
                return True, mth
        else:
            results = process.extract(method_name, self.method_names, limit=3)
            methods = []
            for res in results:
                mth = db.class_index.find({"methods.name": { "$in": [res[0]]}})
                methods.append(mth)
            return False, methods

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
    indexer = CodeIndexer()
    return bot, dictionary, console, stats, mods, indexer

bot, dictionary, console, stats, mods, indexer = create_bot()
bot.remove_command('help')
from .cogs import *

from .event_listeners import *
from .scripts import *

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
    embed = Embed(title="Help Menu", description="Bot Prefix: !")
    embed.add_field(name="!define <word>", value="Define a word quickly from the dictionary")
    embed.add_field(name="!invite", value="Get the permanent invite link")
    embed.add_field(name="!howdoi <your query>", value="Get a StackOverflow snippet by query")
    embed.add_field(name="!mod <mod title>", value="Find links to mods based on a title")
    embed.add_field(name="!wheretostart", value="Find links to the Valheim Modding Wiki easily")
    embed.add_field(name="!template", value="Get an easy plugin class template to copy from")
    embed.add_field(name="!xkcd", value="Get a random xkcd funny")
    embed.add_field(name="!findclass <class>", value="Find info about a class from Valheim")
    embed.add_field(name="!findmethod <method>", value="Find info about a method from Valheim")
    embed.add_field(name="!findfield <field>", value="Find info about a field from Valheim")
    embed.add_field(name="!info", value="Get information about the bot")
    await ctx.message.author.send(embed=embed)

    
def run_bot():
    try:
        bot.run(config.token, bot=True)
    except KeyboardInterrupt:
        embed = Embed(name="He Dead!", description="\u200B", color=0xff0000)
        embed.set_thumbnail(url='https://media.tenor.com/images/aba657f0be4d10fe1996a0ab3dfa72c0/tenor.gif')
        bot.close()
        exit()