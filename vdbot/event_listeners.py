from discord.ext.commands.errors import CommandNotFound
from rich import print
from rich.panel import Panel
from rich.markdown import Markdown
from vdbot import bot, console, stats

@bot.event
async def on_ready():
    console.print(Panel('[bold green]Connected to Discord API ✓\nLoading Complete ✓'), justify='center')
    console.print(Markdown('# Logging Commands:'))

@bot.event
async def on_message(ctx):
    await bot.process_commands(ctx)
    stats.msgs_parsed += 1