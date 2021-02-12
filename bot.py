#!/usr/bin/env python3
#All the imports
import os

import discord
from discord.ext import commands

from string_dec import *
from functions import *

#Grab bot token and server name from other file
TOKEN = DISCORD_TOKEN
GUILD = DISCORD_GUILD

# For some reason setting it up this way allows for easier checking of ID's
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='c!',intents=intents)

maintenance = 0 #Global variable to see if we are down for maintenance

@bot.event
async def on_ready(): #Prints Server name and user ID's for those connected on startup
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
async def on_member_join(member): #On member join PM them a message (Not sure if Kayla wants this)
    await member.create_dm()
    await member.dm_channel.send(
        f'{member.name}' + welcome_str
    )

# HELP COMMAND
@bot.command(pass_context=True)
async def help(ctx): #Displays interactive help menu that shows user available commands
    global maintenance #Maintenance check
    if maintenance:
        curr_page=1
        commands_dict = get_commands(curr_page) #Pulls command list for current page of menu
        max_page=6
        #Sets up the help menu as a fancy embed for formatting
        embed=discord.Embed(title="",description="Click on the # reaction to flip through the pages\n-----------------------------------------------", color=0xff2600)
        embed.set_author(name="Help Menu", icon_url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fknowledgeworks.org%2Fwp-content%2Fuploads%2F2018%2F02%2Fquestion-mark-icon-1.png&f=1&nofb=1")
        for key in commands_dict: #Display commands (special icons for newly added ones)
            if key[:3] == "NEW":
                embed.add_field(name="🆕 c!"+key[3:].replace('_',' '),
                value=commands_dict[key]+"\n-",inline=False)
            else:
                embed.add_field(name="⏹ c!"+key.replace('_',' '),
                value=commands_dict[key]+"\n-",inline=False)
        embed.set_footer(text=help_footer+"| Current Page "+str(curr_page)+"/"+str(max_page))
        help = await ctx.send(embed=embed)
        # Will have to add authority check and different outcomes here
        for emoji in emoji_numbers: #Add the 'menu pages' as reactions
            await help.add_reaction(emoji)
        while 1:
            try:
                #Wait for user to react to the menu and store user info and reaction
                reaction, user = await bot.wait_for('reaction_add',timeout=10)
                react_author = user.name+"#"+user.discriminator
                if react_author == str(ctx.message.author): #only the user who asked for help can change the page
                    # Update the embed to have proper commands shown
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
                    await help.edit(embed=embed) #Actually updates the embed
                    await help.remove_reaction(reaction,user) #Removes user reaction for easier page changing
            except: #Most likely Timeout Error Waiting for a reaction
                #Update footer so user knows they can no longer change page
                embed.set_footer(text=help_footer_done+"| Current Page "+str(curr_page)+"/"+str(max_page))
                await help.edit(embed=embed)
                return
    else: #If Maintenance
        await ctx.send(maintenance_block_text)

#Needs a lot of work once we get sheets settled
@bot.command(name='inventory') #shows user inventory or allows mods to link/view/update inventory info in the bot
async def critter_inventory(ctx,command_ext='NULL',user='NULL',database_tab_name='NULL'):
    global maintenance #maintenance check
    if maintenance:
        user_name = str(ctx.message.author).split('#')[0]
        if command_ext == 'NULL': #Default case, Displays inventory (update w/sheets functionality)
            await ctx.send('Displaying inventory for '+user_name+'!')
        else:
            # WILL ADD AUTHORITY CHECK HERE AND ARG CHECKS
            if command_ext == 'add': # Add a link to local storage
                await ctx.send('Adding inventory tab '+database_tab_name+' for user '+user+'!')
            elif command_ext == 'update': # Update a link in local storage
                await ctx.send('Linking inventory tab '+database_tab_name+' to user '+user+'!')
            elif command_ext == 'view': # View the link in local storage
                await ctx.send('Displaying inventory tab of user '+user+'!')
            else:
                await ctx.send(invalid_command)
    else:
        await ctx.send(maintenance_block_text)

#Needs a lot of work once we get sheets settled
@bot.command(name='tenant')#rolls random tenant and display info (from full list or event list)
async def critter_tenant(ctx,command_ext='NULL'):
    global maintenance #maintenance check
    if maintenance:
        if command_ext=='NULL': #Default case: full list
            await ctx.send('Displaying random tenant!')
        elif command_ext == 'event': # Event list only
            await ctx.send('Displaying random tenant from event list!')
        else: #Anything else is an invalid command
            await ctx.send(invalid_command)
    else:
        await ctx.send(maintenance_block_text)


#Base functionality is there, but it needs proper formatting
@bot.command(name='ping') #Pings the bot to check response time
async def ping(ctx):
    await ctx.send('Pong! {0}ms'.format(round(bot.latency*1000)))

#Base functionality is there, but it needs proper formatting
@bot.command(name='maintenance') #Deactivates bot functionality for maintenance
async def critter_maintenance(ctx,value):
    global maintenance
    if int(value) == 1: #1 Allows commands
        await ctx.send(maintenance_on_text)
        maintenance = int(value)
    elif int(value) == 0: #0 Disallows commands
        await ctx.send(maintenance_off_text)
        maintenance = int(value)
    else: #Anything else is wrong
        await ctx.send(maintenance_wrong_text)

#Needs a lot of work once we get sheets settled
@bot.command(name='injury') #Pull random injury from sheets based on category and "give" to target
async def critter_injury(ctx,target,category):
    global maintenance
    if maintenance: #Maintenance check
        if target == 'random': #Target can be random
            await ctx.send('Choosing random user') #is this from users or tenants or neither
        # Will later actually pull from sheets and randomize stuff
        await ctx.send(target+' has been afflicted with '+category+' (THIS WILL CHANGE)')
    else:
        await ctx.send(maintenance_block_text)

@bot.event
async def on_command_error(ctx, error): #Handles any command errors
    if isinstance(error, discord.ext.commands.errors.CommandNotFound): #Command not found
        await ctx.send(invalid_command)
    elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument): #Missing an argument
        await ctx.send(missed_argument)
    else: #Anything else is unlikely, but problematic
        await ctx.send(serious_error)


bot.run(TOKEN)
