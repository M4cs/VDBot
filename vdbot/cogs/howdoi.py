from howdoi import howdoi
from vdbot import bot
from discord import Embed

allowed_channels = [830501966802321419, 830502092070060122, 830502481846730783, 830545339890532402]

@bot.command(aliases=['howdoi', 'hdi'], help="Get a definition of code query")
async def on_howdoi(ctx, *, query):
    if ctx.channel.id in allowed_channels:
        parser = howdoi.get_parser()
        args = vars(parser.parse_args(query.split(" ")))
        output = howdoi.howdoi(args)
        if len(output) > 2000:
            output = output[0:1997] + "..."
        embed = Embed(title="Query: " + query, description=output, color=0xff0000)
        await ctx.reply(content="", embed=embed, mention_author=True)
    else:
        await ctx.reply(content=f"**Please use this in a development channel only!**", mention_author=True)