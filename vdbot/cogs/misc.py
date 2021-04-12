from vdbot import bot
from discord import Embed
import xkcd, random

@bot.command(aliases=['xkcd', 'afunnypls'], help='Get a random xkcd comic.')
async def on_xkcd(ctx):
    num = random.randint(0, xkcd.getLatestComicNum())
    comic = xkcd.getComic(num)
    url = comic.getImageLink()
    embed = Embed(title="Laugh at this.", description="\u200B")
    embed.set_image(url=url)
    await ctx.reply(embed=embed)