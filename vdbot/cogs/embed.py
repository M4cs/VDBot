from vdbot import bot
from discord import Embed

allowed_users = [368083908862017537, 830587634110693388, 524039295317835797]

@bot.command('code')
async def on_code(ctx, *, code):
    code_lines = code.split('\n')
    max_spaces = 0
    if code_lines[0].startswith(' '):
        for x in code_lines[0]:
            if x == ' ':
                max_spaces += 1
            else:
                break
    elif code_lines[1].startswith(' '):
        for x in code_lines[1]:
            if x == ' ':
                max_spaces += 1
            else:
                break
    for i, code_line in enumerate(code_lines):
        if code_line.startswith(' '):
            code_lines[i] = code_line[max_spaces:]
    await ctx.message.delete()
    code = '```cs\n' + '\n'.join(code_lines) + '\n```'
    embed = Embed(title=f"Code Snippet", description=f"Posted by <@{ctx.author.id}>")
    embed.add_field(name="\u200B", value=code)
    await ctx.channel.send(embed=embed)

@bot.command(aliases=['embed', 'e'], help="Embed a message")
async def on_embed(ctx, title, *, text):
    if ctx.message.author.id in allowed_users:
        embedVar = Embed(title=title, description=text, color=0x000000)
        await ctx.channel.send(content="", embed=embedVar)
    else:
        await ctx.channel.send(content="**You do not have permission to use that command**")

@bot.command(aliases=['template'], help='A template for Valheim Plugins')
async def on_template(ctx):
    embed = Embed(title="Valheim Modding Template", description="This code can be useful for anybody needing a base template for their plugin class.")
    async with ctx.message.channel.typing():
        embed.add_field(name="Requirements:", value="- References to HarmonyLib and BepInEx\n- A .NET Class Library Project")
    await ctx.reply(content="""
```cs
using BepInEx;
using HarmonyLib;
using System.Reflection;

namespace PluginNamespace {

    [BepInPlugin(pluginGUID, pluginName, pluginVersion)]
    class Main : BaseUnityPlugin {
        public const string pluginGUID = "com.yourname.PluginName";
        public const string pluginName = "PluginName";
        public const string pluginVersion = "1.0.0";

        public void Awake() {
            Harmony harmony = new Harmony(pluginGUID);
            harmony.PatchAll(Assembly.GetExecutingAssembly());
        }
    }
}```""", embed=embed, mention_author=True)
