from vdbot import bot
from discord import Embed

allowed_users = [368083908862017537, 830587634110693388, 524039295317835797]

@bot.command(aliases=['embed', 'e'], help="Embed a message")
async def on_embed(ctx, title, *, text):
    if ctx.message.author.id in allowed_users:
        embedVar = Embed(title=title, description=text, color=0x000000)
        await ctx.channel.send(content="", embed=embedVar)
    else:
        await ctx.channel.send(content="**You do not have permission to use that command**")