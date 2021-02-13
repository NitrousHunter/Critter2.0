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
MODS = DISCORD_MOD_CHANNEL

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

# HELP COMMAND PAGE 3 COMMAND 4
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

# INVENTORY COMMANDS PAGE 1 COMMAND 1, PAGE 6 COMMANDS 1,2 and 3
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
            if command_ext.lower() == 'add': # Add a link to local storage
                if user == 'NULL' or database_tab_name == 'NULL': # Argument verification
                    arg_txt = "user name or database tab name"
                    await ctx.send(missed_argument+arg_txt+missed_argument_2)
                    return
                await ctx.send('Adding inventory tab '+database_tab_name+' for user '+user+'!')
            elif command_ext.lower() == 'update': # Update a link in local storage
                if user == 'NULL' or database_tab_name == 'NULL': # Argument verification
                    arg_txt = "user name or database tab name"
                    await ctx.send(missed_argument+arg_txt+missed_argument_2)
                    return
                await ctx.send('Linking inventory tab '+database_tab_name+' to user '+user+'!')
            elif command_ext.lower() == 'view': # View the link in local storage
                if user == 'NULL': # Argument verification
                    arg_txt = "user name"
                    await ctx.send(missed_argument+arg_txt+missed_argument_2)
                    return
                await ctx.send('Displaying inventory tab of user '+user+'!')
            else:
                await ctx.send(invalid_command)
    else:
        await ctx.send(maintenance_block_text)

# BALANCE COMMANDS PAGE 1 COMMAND 2 and 3
#Needs a lot of work once we get sheets settled
@bot.command(name='balance') #Shows user balance or global leaderboards of $
async def critter_balance(ctx,command_ext='NULL'):
    global maintenance #maintenance check
    if maintenance:
        if command_ext == 'NULL': #Default case is user's balance
            user_name = str(ctx.message.author)
            await ctx.send('Displaying the balance of user: '+user_name)
        elif command_ext.lower() == 'top': #Top indicates we want leaderboards
            await ctx.send('Displaying the leaderboards of balance')
        else:
            await ctx.send(invalid_command)
    else:
        await ctx.send(maintenance_block_text)

# SHOP COMMANDS PAGE 1 COMMANDS 4 and 5
#Needs a lot of work once we get sheets settled
@bot.command(name='shop') #Bot displays the shop page specified
async def critter_shop(ctx,page_num=0): #Default case is menu that shows pages
    global maintenance #maintenance check
    if maintenance:
        curr_page = int(page_num) #Will need to access sheets to pull real data
        await ctx.send('Displaying shop page:'+str(curr_page)+'! (0 is menu)')
    else:
        await ctx.send(maintenance_block_text)

# BUY COMMAND PAGE 1 COMMAND 6
#Needs a lot of work once we get sheets settled
@bot.command(name='buy') #Bot buys the specified quantity of specified item
async def critter_buy(ctx,item,quantity):
    global maintenance #maintenance check
    if maintenance:
        user_name = str(ctx.message.author)
        #Needs to pull from sheets and confirm valid item as well as user has right balance
        await ctx.send(user_name + 'is buying '+str(quantity)+'x '+str(item)+' from the shop!')
        #Needs to deduct cost of items from user inventory
    else:
        await ctx.send(maintenance_block_text)

# SELL COMMAND PAGE 2 COMMAND 1
#Needs a lot of work once we get sheets settled
@bot.command(name='sell') #Bot buys the specified quantity of specified item
async def critter_sell(ctx,item,quantity):
    global maintenance #maintenance check
    if maintenance:
        user_name = str(ctx.message.author)
        #Needs to pull from sheets and confirm valid item as well as user has right quantity
        await ctx.send(user_name + 'is selling '+str(quantity)+'x '+str(item)+' to the shop!')
        #Needs to add cost of the items to user inventory
    else:
        await ctx.send(maintenance_block_text)

# GIFT COMMAND PAGE 2 COMMAND 2
#Needs a lot of work once we get sheets settled
@bot.command(name='gift') #Bot gifts the target user a specified quantity of specified item
async def critter_gift(ctx,user,item,quantity):
    global maintenance #maintenance check
    if maintenance:
        user_name = str(ctx.message.author)
        #Needs to pull from sheets and confirm valid item as well as user has right quantity
        await ctx.send(user_name + 'is giving '+user+' '+str(quantity)+'x '+str(item)+'!')
        #Needs to deduct items from caller inventory, then give to user inventory
        #Also needs a confirm/reject menu in reactions
    else:
        await ctx.send(maintenance_block_text)

# EXCHANGE SHARDS COMMAND COMMAND PAGE 2 COMMAND 3
#Needs a lot of work once we get sheets settled
@bot.command(name='exchange') #Bot exchanges the specified quantity of shards for PD
async def critter_exchange(ctx,command_ext,quantity):
    global maintenance #maintenance check
    if maintenance:
        if command_ext.lower() == 'shards': #Only case is exchange shards
            user_name = str(ctx.message.author)
            await ctx.send(user_name+' is exchanging '+str(quantity)+'shards fo PD!')
            #Needs to deduct shards from inventory and add PD
        else: #No other use of "exchange" primary command
            await ctx.send(invalid_command)
    else:
        await ctx.send(maintenance_block_text)

# TENANT COMMANDS PAGE 2 COMMANDS 4 and 5
#Needs a lot of work once we get sheets settled
@bot.command(name='tenant')#rolls random tenant and display info (from full list or event list)
async def critter_tenant(ctx,command_ext='NULL'):
    global maintenance #maintenance check
    if maintenance:
        if command_ext=='NULL': #Default case: full list
            await ctx.send('Displaying random tenant!')
        elif command_ext.lower() == 'event': # Event list only
            await ctx.send('Displaying random tenant from event list!')
        else: #Anything else is an invalid command
            await ctx.send(invalid_command)
    else:
        await ctx.send(maintenance_block_text)

# SUGGEST COMMAND PAGE 2 COMMAND 6
#Base functionality is there, but it needs proper formatting
@bot.command(name='suggest')#User makes a suggestion to the mods
async def critter_suggest(ctx,*,suggestion):
    global maintenance #maintenance check
    if maintenance:
        user_name = str(ctx.message.author)
        await ctx.message.delete() #Hide user suggestion from others
        #Is there feedback to the user that the mod got their suggestion?
        channel = bot.get_channel(MODS)
        await channel.send(user_name+' suggests "'+suggestion+'"') #Give user suggestion to the mods
    else:
        await ctx.send(maintenance_block_text)

# BUG REPORT COMMAND PAGE 3 COMMAND 1
#Base functionality is there, but it needs proper formatting
@bot.command(name='bug')#User makes a bug_report to the mods
async def critter_bug(ctx,command_ext,*,report):
    global maintenance #maintenance check
    if maintenance:
        if command_ext.lower()=="report": #only case for bug is report
            user_name = str(ctx.message.author)
            await ctx.message.delete() #Hide user bug report from others
            #Is there feedback to the user that the mod got their report?
            channel = bot.get_channel(MODS)
            await channel.send(user_name+' reported the following bug "'+report+'"')
            #Give bug report to the mods
        else: #no other case for primary command bug
            await ctx.send(invalid_command)
    else:
        await ctx.send(maintenance_block_text)

# JOIN COMMAND PAGE 3 COMMAND 2
#Needs a lot of work once we get sheets settled
@bot.command(name='join') #User adds themselves to role specified (in google sheet)
async def critter_join(ctx,role_name):
    global maintenance #maintenance check
    if maintenance:
        user_name = str(ctx.message.author)
        await ctx.send(user_name+' added themselves to the '+role_name+' role!')
        #Needs to change roles on sheet to reflect this
    else:
        await ctx.send(maintenance_block_text)

# LEAVE COMMAND PAGE 3 COMMAND 3
#Needs a lot of work once we get sheets settled
@bot.command(name='leave') #User removes themselves from role specified (in google sheet)
async def critter_leave(ctx,role_name):
    global maintenance #maintenance check
    if maintenance:
        user_name = str(ctx.message.author)
        await ctx.send(user_name+' removed themselves from the '+role_name+' role!')
        #Needs to change roles on sheet to reflect this
    else:
        await ctx.send(maintenance_block_text)

# PING COMMAND PAGE 3 COMMAND 5
#Base functionality is there, but it needs proper formatting
@bot.command(name='ping') #Pings the bot to check response time
async def critter_ping(ctx):
    global maintenance #maintenance check
    if maintenance:
        await ctx.send('Pong! {0}ms'.format(round(bot.latency*1000)))
    else:
        await ctx.send(maintenance_block_text)

# KEY COMMANDS PAGE 4 COMMANDS 1,2, and 3
#Needs a lot of work once we get sheets settled
@bot.command(name='key') #Mod adds views or deletes to/from key total
async def critter_key(ctx,command_ext='NULL',user_name='NULL',quantity='0'):
    global maintenance #maintenance check
    if maintenance:
        # WILL ADD AUTHORITY CHECK HERE
        if command_ext.lower() == 'add': # Add quantity keys to user_name's total
            if user_name == 'NULL' or quantity == '0': # Argument verification
                arg_txt = "user name or key quantity"
                await ctx.send(missed_argument+arg_txt+missed_argument_2)
                return
            await ctx.send('Adding '+quantity+' keys to '+user_name+"'s total!")
        elif command_ext.lower() == 'delete': #Delete quantity keys from user_name's total
            if user_name == 'NULL' or quantity == '0': # Argument verification
                arg_txt = "user name or key quantity"
                await ctx.send(missed_argument+arg_txt+missed_argument_2)
                return
            await ctx.send('Deleting '+quantity+' keys from '+user_name+"'s total'!")
        elif command_ext.lower() == 'view': # View the key total of user_name
            if user_name == 'NULL': # Argument verification
                arg_txt = "user name"
                await ctx.send(missed_argument+arg_txt+missed_argument_2)
                return
            await ctx.send('Viewing '+user_name+"'s key total!")
        else:
            await ctx.send(invalid_command)
    else:
        await ctx.send(maintenance_block_text)

# INVESTIGATE COMMAND PAGE 4 COMMAND 4
#Needs a lot of work once we get sheets settled
@bot.command(name='investigate') #User investigates a specified location (with an optional item)
async def critter_investigate(ctx,location_name,optional_item='NULL'):
    global maintenance #maintenance check
    if maintenance:
        user_name = str(ctx.message.author)
        if optional_item == 'NULL':
            await ctx.send(user_name+' is investigating the '+location_name)
        else:
            await ctx.send(user_name+' is investigating the '+location_name
            +' using the '+optional_item)
        #Needs to use sheets to do this
    else:
        await ctx.send(maintenance_block_text)

# HORROR COMMAND PAGE 4 COMMAND 5
#Needs a lot of work once we get sheets settled
@bot.command(name='horror') #User fights a horror of specified type
async def critter_horror(ctx,horror_type,courage_level,optional_item='NULL',optional_curse='NULL'):
    global maintenance #maintenance check
    if maintenance:
        user_name = str(ctx.message.author)
        if optional_item == 'NULL' and optional_curse == 'NULL':
            # If no item specified and no curse specified
            await ctx.send(user_name+' (courage level:'+courage_level+
            ') fights a '+horror_type+' with no items or curses!')
        elif optional_item == 'NULL': #Item was not specified, but curse was
            await ctx.send(user_name+' (courage level:'+courage_level+
            ') fights a '+horror_type+' using no item and has '+optional_curse)
        elif optional_curse == 'NULL': #Item was specified, but curse was not
            await ctx.send(user_name+' (courage level:'+courage_level+
            ') fights a '+horror_type+' using the '+optional_item)
        else: #Item and curse specified
            await ctx.send(user_name+' (courage level:'+courage_level+
            ') fights a '+horror_type+' using the '+optional_item
            +' and has '+optional_curse)
        #Needs to use sheets to do this; Do I need a case for no item, but curse?
    else:
        await ctx.send(maintenance_block_text)

# CURSE COMMAND PAGE 4 COMMAND 6
#Needs a lot of work once we get sheets settled
@bot.command(name='curse') #Re-roll curse that came from horror of specified type
async def critter_curse(ctx,horror_type):
    global maintenance #maintenance check
    if maintenance:
        await ctx.send(user_name+' is rerolling a curse from a '+horror_type)
        #Needs to use sheets to do this; Make it modular and can use it in Horror above
    else:
        await ctx.send(maintenance_block_text)

# HATCH COMMAND PAGE 5 COMMAND 1
#Needs a lot of work once we get sheets settled
@bot.command(name='hatch') #Hatch a specified number of eggs (optionally fusions or color swap)
async def critter_hatch(ctx,egg_num,fusion='NULL',color_swap='NULL'):
    global maintenance #maintenance check
    if maintenance:
        user_name = str(ctx.message.author)
        if fusion == "NULL" and color_swap == "NULL": # If no fusion and no color swap
            await ctx.send(user_name+' is hatching '+egg_num+" eggs!")
        elif fusion == "NULL": # If no fusion, but color swap
            await ctx.send(user_name+' is hatching '+egg_num+' eggs and they are color swapped!')
        elif color_swap == "NULL": # If no color swap, but fusion
            await ctx.send(user_name+' is hatching '+egg_num+' eggs and they are fusions!')
        else: # If both color swap and fusion
            await ctx.send(user_name+' is hatching '+egg_num+' eggs and they are fusions and color swapped!')
        #Needs to use sheets to do this (don't forget shiny chance with non-swapped eggs)
    else:
        await ctx.send(maintenance_block_text)

# GACHA COMMAND PAGE 5 COMMAND 2
#Needs a lot of work once we get sheets settled
@bot.command(name='gacha') #Roll a random Gacha when a user redeems a gacha ticket
async def critter_gacha(ctx):
    global maintenance
    if maintenance: #Maintenance check
        await ctx.send("Rolling a random gacha!")
        #Need to integrate with sheets
    else:
        await ctx.send(maintenance_block_text)

# GACHA COMMAND PAGE 5 COMMAND 3
#Needs a lot of work once we get sheets settled
@bot.command(name='voucher') #ROlls a value for a PD voucher when redeemed
async def critter_voucher(ctx,user='NULL'):
    global maintenance
    if maintenance: #Maintenance check
        if user == "NULL":
            await ctx.send("Rolling a PD voucher's value! Don't forget to add to inventory!")
            #Need to integrate with sheets
        else:
            await ctx.send("Rolling a PD voucher's value! Adding to inventory of "+user+"!")
            #Need to integrate with sheets
    else:
        await ctx.send(maintenance_block_text)

# MAINTENANCE COMMAND PAGE 6 COMMAND 4
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

# INJURY COMMAND PAGE 6 COMMAND 5
#Needs a lot of work once we get sheets settled
@bot.command(name='injury') #Pull random injury from sheets based on category and "give" to target
async def critter_injury(ctx,target,category):
    global maintenance
    if maintenance: #Maintenance check
        if target.lower() == 'random': #Target can be random
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
        arg_txt = find_args(ctx.message.content)
        await ctx.send(missed_argument+arg_txt+missed_argument_2)
    else: #Anything else is unlikely, but problematic
        await ctx.send(serious_error)
        print(error)
        channel = bot.get_channel(MODS)
        await channel.send(serious_error_mods)


bot.run(TOKEN)
