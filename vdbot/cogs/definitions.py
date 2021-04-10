from vdbot.cogs import embed
from vdbot import bot, dictionary
from discord import Embed

@bot.command(aliases=['define', 'd'], help='Define a word')
async def on_define(ctx, *, text):
    index = 0
    async with ctx.message.channel.typing():
        result = dictionary.meaning(text)
        embed = Embed(title="Word: " + text)
        for k, v in result.items():
            res = ""
            count = 0 
            for defin in v:
                if count == 3:
                    break
                res += "- " + defin.capitalize() + "\n"
                count += 1
            embed.insert_field_at(index, name=k, value=res, inline=True)
            index += 3
    await ctx.channel.send(content="<@" + str(ctx.message.author.id) + ">", embed=embed)
