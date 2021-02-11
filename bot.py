#!/usr/bin/env python3
import os

import discord
from discord.ext import commands

from string_dec import *
from functions import *

TOKEN = DISCORD_TOKEN
GUILD = DISCORD_GUILD

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='c!',intents=intents)

maintenance = 0

@bot.event
async def on_ready():
    global maintenance
    maintenance = 1
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

bot.remove_command('help')

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'{member.name}' + welcome_str
    )


# HELP COMMAND
@bot.command(pass_context=True)
async def help(ctx):
    global maintenance
    if maintenance:
        global menu_wait
        curr_page=1
        commands_dict = get_commands(curr_page)
        max_page=6
        embed=discord.Embed(title="",description="Click on the # reaction to flip through the pages\n-----------------------------------------------", color=0xff2600)
        embed.set_author(name="Help Menu", icon_url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fknowledgeworks.org%2Fwp-content%2Fuploads%2F2018%2F02%2Fquestion-mark-icon-1.png&f=1&nofb=1")
        for key in commands_dict:
            if key[:3] == "NEW":
                embed.add_field(name="🆕 c!"+key[3:].replace('_',' '),
                value=commands_dict[key]+"\n-",inline=False)
            else:
                embed.add_field(name="⏹ c!"+key.replace('_',' '),
                value=commands_dict[key]+"\n-",inline=False)
        embed.set_footer(text=help_footer+"| Current Page "+str(curr_page)+"/"+str(max_page))
        help = await ctx.send(embed=embed)
        for emoji in emoji_numbers:
            await help.add_reaction(emoji)
        while 1:
            try:
                reaction, user = await bot.wait_for('reaction_add',timeout=10)
                if user.name != BOTNAME:
                    curr_page = emoji_numbers.index(reaction.emoji) + 1
                    commands_dict = get_commands(curr_page)
                    #print ("Bot should change to page " + str(curr_page) + " for user " +user.name) # Debug statement
                    embed=discord.Embed(title="",description="Click on the # reaction to flip through the pages\n-----------------------------------------------", color=0xff2600)
                    embed.set_author(name="Help Menu", icon_url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fknowledgeworks.org%2Fwp-content%2Fuploads%2F2018%2F02%2Fquestion-mark-icon-1.png&f=1&nofb=1")
                    for key in commands_dict:
                        if key[:3] == "NEW":
                            embed.add_field(name="🆕 c!"+key[3:].replace('_',' '),
                            value=commands_dict[key]+"\n-",inline=False)
                        else:
                            embed.add_field(name="⏹ c!"+key.replace('_',' '),
                            value=commands_dict[key]+"\n-",inline=False)
                    embed.set_footer(text=help_footer+"| Current Page "+str(curr_page)+"/"+str(max_page))
                    await help.edit(embed=embed)
            except: #Most likely Timeout Error Waiting for a reaction
                embed.set_footer(text=help_footer_done+"| Current Page "+str(curr_page)+"/"+str(max_page))
                await help.edit(embed=embed)
                return
    else: #If Maintenance
        await ctx.send(maintenance_block_text)


@bot.command(name='tenant',  help="tenant help")
async def critter_tenant(ctx,):
    global maintenance
    if maintenance:
        await ctx.send('Executing tenant!')
    else:
        await ctx.send(maintenance_block_text)

@bot.command(name='tenant add', help="tenant add help")
async def critter_tenant_add(ctx):
    global maintenance




@bot.command(name='maintenance')
async def critter_maintenance(ctx,value=2):
    global maintenance
    if int(value) == 1:
        await ctx.send(maintenance_on_text)
        maintenance = int(value)
    elif int(value) == 0:
        await ctx.send(maintenance_off_text)
        maintenance = int(value)
    else:
        await ctx.send(maintenance_wrong_text)

bot.run(TOKEN)
