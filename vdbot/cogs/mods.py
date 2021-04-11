from discord.embeds import Embed
from vdbot import bot, mods, console

@bot.command(aliases=['mod', 'findmod'])
async def on_find_mods(ctx, *, query):
    async with ctx.channel.typing():
        results = mods.find_mods(query)
        embed = Embed(title="Mod Results:", description="Here's what I could find on Nexusmods (TS Coming Soon):")
        for result in results:
            embed.add_field(name=result['name'],
            value="**Summary**\n" + result['data']['summary'] + "\n**Link:** " + result['data']['url'], inline=False)
    await ctx.reply(embed=embed)
        

