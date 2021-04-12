import traceback
from discord.embeds import Embed
from discord.ext.commands.errors import CommandError, CommandNotFound
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
    embed = Embed(title="Good Morning", description="It's a beautiful day for pie", color=0x00ff00)
    embed.set_image(url="https://media1.tenor.com/images/4443069022c0e23622626a46909162ec/tenor.gif?itemid=10618052")
    await bot.get_channel(830932320771899432).send(embed=embed)

@bot.event
async def on_message(ctx):
    await bot.process_commands(ctx)
    stats.msgs_parsed += 1

@bot.event
async def on_command_error(ctx, error):
    e = str(error)
    await ctx.reply(content="Error: " + e)



@bot.event
async def on_error(event , *args, **kwargs):
    message = args[0]
    console.print(Panel('[bold red]Error Failure![/bold red]'), justify='center')
    console.print(Panel('[bold red]' + traceback.format_exc(limit=2) + "[/bold red]"), justify='center')
    embed = Embed(title="New Error!", description=f"**Thrown By**: <@{str(message.author.id)}>\n**Channel:** {str(message.channel.id)}\n\n```{str(traceback.format_exc(limit=2))}```")
    await bot.get_channel(830932320771899432).send(embed=embed, content="<@368083908862017537>")
    