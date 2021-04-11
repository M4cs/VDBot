from discord.embeds import Embed
from vdbot import bot, mods, console
from discord.ext import commands

@bot.command(aliases=['mod', 'findmod'])
async def on_find_mods(ctx, *, query):
    if not mods.is_reindexing:
        async with ctx.channel.typing():
            results = mods.find_mods(query)
            embed = Embed(title="Mod Results:", description="Here's what I could find on Nexusmods and Thunderstore")
            for result in results:
                embed.add_field(name=result['name'],
                value="**Summary**\n" + result['data']['summary'] + "\n**Nexus Link:** " + result['data']['url'], inline=False)
        await ctx.reply(embed=embed)
    else:
        await ctx.reply(content="**I'm reindexing right now, try again in 10 seconds!**")
        
@bot.command(aliases=['updateindex'])
async def on_update_index(ctx):
    if ctx.message.author.id in [368083908862017537, 830587634110693388, 524039295317835797]:
        async with ctx.channel.typing():
            await ctx.reply(content="Updating Indexes...")
            mods.update_index()
        await ctx.reply(content="Updated Indexes!")


