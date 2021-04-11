from vdbot import bot, stats
from discord import Embed
from discord.ext import commands

@bot.command(aliases=['wiki', 'wheretostart', 'wts'])
async def on_wiki(ctx):
    async with ctx.channel.typing():
        embed = Embed(title="Valheim Modding", 
        description="Checkout the Valheim Modding Wiki here which has a ton of useful information and guides written by members of the community!", 
        url="https://github.com/Valheim-Modding/Wiki", color=0xff0000)
        embed.add_field(name="Getting Started with Visual Studio", value="https://github.com/Valheim-Modding/Wiki/wiki/Getting-started-with-Visual-Studio", inline=False)
        embed.add_field(name="Unity Project Guide", value="https://github.com/Valheim-Modding/Wiki/wiki/Valheim-Unity-Project-Guide", inline=False)
        embed.add_field(name="BepInEx Plugin Best Practices", value="https://github.com/Valheim-Modding/Wiki/wiki/BepInEx-Plugin-Best-Practices", inline=False)
    await ctx.reply(content="", embed=embed, mention_author=True)

@bot.command(aliases=['info', 'yggdrasil'])
@commands.has_role("Moderator")
async def on_info(ctx):
    embed = Embed(title="Böt of Yggdrasil", description="Discord Bot for Valheim Modding Discord")
    async with ctx.channel.typing():
        days, hours, minutes, seconds = stats.get_uptime()
        uptime_str = ""
        if days > 0:
            uptime_str = uptime_str + str(days) + " d, "
        if hours > 0:
            uptime_str = uptime_str + str(hours) + " hr, "
        if minutes > 0:
            uptime_str = uptime_str + str(minutes) + " min, "
        uptime_str = uptime_str + str(seconds) + " sec"
        embed.add_field(name="🕖 Uptime", value=uptime_str)
        embed.add_field(name="🔢 Version", value="1.0", inline=True)
        embed.add_field(name="💻 Commands Loaded", value=str(len(bot.commands)), inline=True)
        embed.add_field(name="📝 Messages Parsed", value=str(stats.msgs_parsed), inline=True)
        embed.add_field(name="🏃‍♂️ Commands Run", value=str(stats.command_count), inline=True)
    await ctx.reply(embed=embed)
