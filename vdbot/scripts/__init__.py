from dataclasses import field
from discord.embeds import Embed
from vdbot.db import db
from vdbot import bot, indexer, console
import json


@bot.command(aliases=['findclass', 'class'])
async def on_findclass(ctx, class_name):
    found, results = indexer.find_class(class_name)
    if found:
        should_dm = False
        method_names = ', '.join([x['name'] for x in results['methods']])
        field_names = ', '.join([x['name'] for x in results['fields']])
        if len(method_names) + len(field_names) > 1900:
            should_dm = True
        console.print(len(method_names), justify='center')
        console.print(len(field_names), justify='center')
        console.print(should_dm, justify='center')
        if not should_dm:
            embed = Embed(
                title=results['name'],
                description=f"""**Method Names:** {method_names}\n**Field Names:** {field_names}""")
            await ctx.reply(embed=embed)
        else:
            method_name_msgs = []
            field_name_msgs = []
            current_count = 0
            current_method_string = ""
            current_field_string = ""
            for method in results['methods']:
                if current_count == 500:
                    method_name_msgs.append(current_method_string)
                    current_count = 0
                    current_method_string = ""
                if current_count != 0:
                    current_method_string += ", "
                current_method_string += method['name']
                current_count += len(method['name'])
            current_count = 0
            if current_method_string != "":
                method_name_msgs.append(current_method_string)
            for field in results['fields']:
                if current_count == 500:
                    field_name_msgs.append(current_field_string)
                    current_count = 0
                    current_field_string = ""
                if current_count != 0:
                    current_field_string += ", "
                current_field_string += field['name']
                current_count += len(field['name'])
            if current_field_string != "":
                field_name_msgs.append(current_field_string)
            for method_msg in method_name_msgs:
                console.print(len(method_msg))
                embed = Embed(title=results['name'],
                description="**Method Names:** " + method_msg)
                await ctx.message.author.send(embed=embed)
            for field_msg in field_name_msgs:
                embed = Embed(title=results['name'],
                description="**Field Names:** " + field_msg)
                await ctx.message.author.send(embed=embed)
            await ctx.reply("**Class too big. Sent to your DMs!**")
    else:
        await ctx.reply("Could not find class. Possible meanings " + str(results))

@bot.command(aliases=['findfield', 'field'])
async def on_findfield(ctx, field_name):
    found, results = indexer.find_field(field_name)
    if found:
        if results.count() > 1:
            embed = Embed(title="Ambiguous Match Found!", description="This Field Was Found In Multiple Classes!")
            embed.add_field(name="Matches:", value=', '.join([x['name'] + "." + field_name for x in results]))
            await ctx.reply(embed=embed)
        else:
            if '.' in field_name:
                field_name = field_name.split('.')[-1]
            our_field = None
            class_name = results[0]['name']
            for res in results:
                for field in res['fields']:
                    if field['name'] == field_name:
                        our_field = field
                        break
            embed = Embed(title="**Field:** " + class_name + "." + field_name, description=f"**Field Type:** {our_field['type']}\n**Is Private:** {'True' if our_field['is_private'] else 'False'}")
            await ctx.reply(embed=embed)
    else:
        names = []
        for res in results:
            for r in res:
                if r['name'] not in names:
                    names.append(r['name'])
        await ctx.reply(embed=Embed(title="Could not find field", description="Check CaSe!\nPossible classes to look at: " + ', '.join(names)))



@bot.command(aliases=['findmethod', 'method'])
async def on_findmethod(ctx, method_name):
    found, results = indexer.find_method(method_name)
    if found:
        if results.count() > 1:
            embed = Embed(title="Ambiguous Match Found!", description="This Method Was Found In Multiple Classes!")
            embed.add_field(name="Matches:", value=', '.join(x['name'] + '.' + method_name.capitalize() for x in results))
            await ctx.reply(embed=embed)
        else:
            if '.' in method_name:
                method_name = method_name.split('.')[-1]
            our_method = None
            class_name = results[0]['name']
            for res in results:
                for method in res['methods']:
                    if method['name'] == method_name:
                        our_method = method
                        break
            params = []
            if len(our_method['parameters']) > 0:
                for param in our_method['parameters']:
                    params.append(param['name'] + ": " + param['type'])
            embed = Embed(title="**Method:** " + class_name + "." + method_name, description=f"**Return Type:** {our_method['type']}\n**Is Private:** {'True' if our_method['is_private'] else 'False'}\n**Parameters:** {', '.join(params) if len(params) > 0 else 'No Params'}")
            await ctx.reply(embed=embed)
    else:
        names = []
        for res in results:
            for r in res:
                if r['name'] not in names:
                    names.append(r['name'])

        await ctx.reply(embed=Embed(title="Could not find method", description="Check CaSe!\nPossible classes to look at: " + ', '.join(names)))

@bot.command(aliases=['codereindex'])
async def on_codereindex(ctx):
    if ctx.message.author.id == 368083908862017537:
        await ctx.reply('**Reindexing Code**')
        with open('vdbot/scripts/codeindex.json', 'r+') as f:
            obj = json.loads(f.read())
            for clss in obj['classes']:
                clss_obj = {
                    'name': clss.get('name'),
                    'namespace': clss.get('namespace'),
                    'methods': [],
                    'fields': []
                }
                for method in clss.get('methods'):
                    method_obj = {
                        'name': method.get('name'),
                        'type': method.get('type'),
                        'is_private': method.get('is_private'),
                        'parameters': []
                    }
                    if method.get('parameters'):
                        for param in method['parameters']:
                            method_obj['parameters'].append({
                                'name': param.get('name'),
                                'type': param.get('type')
                            })
                    clss_obj['methods'].append(method_obj)
                for field in clss.get('fields'):
                    field_obj = {
                        'name': field.get('name'),
                        'type': field.get('type'),
                        'is_private': field.get('is_private')
                    }
                    clss_obj['fields'].append(field_obj)
                db.class_index.insert(clss_obj)
        await ctx.reply('**Finished Migrating**')

