from vdbot import bot
from discord import Embed

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