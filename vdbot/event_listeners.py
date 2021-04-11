from discord.embeds import Embed
from discord.ext.commands.errors import CommandNotFound
from rich import print
from rich.panel import Panel
from rich.markdown import Markdown
from vdbot import bot, console, stats
from vdbot.constants import WELCOME_MSG

@bot.event
async def on_member_join(member):
    embed = Embed(title="Welcome to the Valheim Modding Discord",
    description=WELCOME_MSG)
    await member.send(embed=embed)

@bot.event
async def on_ready():
    console.print(Panel('[bold green]Connected to Discord API ✓\nLoading Complete ✓'), justify='center')
    console.print(Markdown('# Logging Commands:'))

@bot.event
async def on_message(ctx):
    await bot.process_commands(ctx)
    stats.msgs_parsed += 1