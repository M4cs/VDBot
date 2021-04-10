from vdbot import bot
from discord import Embed

@bot.command(aliases=['embed', 'e'], help="Embed a message")
async def on_embed(ctx, title, *, text):
    embedVar = Embed(title=title, description=text, color=0x000000)
    await ctx.channel.send(content="", embed=embedVar)