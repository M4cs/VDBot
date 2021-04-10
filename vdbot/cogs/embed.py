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

@bot.command(aliases=['template'], help='A template for Valheim Plugins')
async def on_template(ctx):
    embed = Embed(title="Valheim Modding Template", description="The following code can be useful for anybody needing a base template for their plugin class.")
    async with ctx.message.channel.typing():
        embed.add_field(name="Requirements:", value="- References to HarmonyLib and BepInEx\n- A .NET Class Library Project")
        embed.add_field(name="Template", value="""
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
        Harmony harmony;

        public void Awake() {
            harmony = new Harmony(pluginGUID);
            harmony.PatchAll(Assembly.GetExecutingAssembly());
        }
    }
}"""
        )
    await ctx.message.send(content="", embed=embed)
