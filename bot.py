#!/usr/bin/env python3
#All the imports
import os
from datetime import datetime, timedelta
import asyncio
import nest_asyncio
import math

import random
import discord
from discord.ext import tasks,commands

from string_dec import *
from functions import *

#Grab bot token and server name from other file
TOKEN = DISCORD_TOKEN
GUILD = DISCORD_GUILD
MODS = DISCORD_MOD_CHANNEL
WELCOME = DISCORD_WELCOME_CHANNEL
BIRTHDAY_CHAN = DISCORD_BIRTHDAY_CHANNEL
INVESTIGATE_CHAN = DISCORD_INVESTIGATION_CHANNEL
SEASON_CHAN = DISCORD_SEASON_CHANNEL

# For some reason setting it up this way allows for easier checking of ID's
intents = discord.Intents.default()
intents.members = True
#intents.guilds = False
intents.bans = False
intents.emojis = False
intents.integrations = False
intents.webhooks = False
intents.invites = False
intents.voice_states = False
#intents.guild_messages = False
#intents.dm_messages = False
#intents.guild_reactions = False
intents.dm_reactions = False
intents.guild_typing = False
intents.dm_typing = False
bot = commands.Bot(command_prefix='c!',intents=intents)

maintenance = 0 #Global variable to see if we are down for maintenance
guild_index = 0 #Global index of primary discord server for the bot

nest_asyncio.apply()

def validate_role(user,role_name):
    role_name = str(role_name)
    role = discord.utils.find(lambda r: r.name == role_name, bot.guilds[guild_index].roles)
    if role in user.roles:
        return True
    else:
        return False

@bot.event
async def on_ready(): #Prints Server name and user ID's for those connected on startup
    global maintenance
    global guild_index
    for guild in bot.guilds:
        if guild.name == GUILD:
            guild_index = bot.guilds.index(guild)
            break

    guild = bot.guilds[guild_index]

    print(
        f'{bot.user} is connected to the following primary guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')
    init_sheets()
    if update_timing.is_running():
        print("Caught an error!")
        update_timing.cancel()
        update_timing.restart()
    else:
        update_timing.start()
    maintenance = 1

bot.remove_command('help')

@bot.event
async def on_member_join(member): #On member join stick message in intro channel
    if member.guild.id == bot.guilds[guild_index].id:
        channel = bot.get_channel(WELCOME) #Grab channel info based on id
        await channel.send(welcome_str % (f'{member.id}',str(DISCORD_GENERAL_INTRO_CHANNEL)))
        #Send message to channel

# HELP COMMAND PAGE 1 COMMAND 1
@commands.has_any_role("Ghosts","Tenants","Interns","Mods","Dev")
@bot.command(name='help',pass_context=True,ignore_extra=False)
async def critter_help(ctx,page_num='1'): #Displays interactive help menu that shows user available commands
    global maintenance #Maintenance check
    if maintenance:
        if not page_num.isdigit():
            await ctx.send(embed=send_error_msg("Error: Help Page Not Found",page_error_text))
            return
        curr_page=int(page_num)
        if get_commands(curr_page) == -1:
            await ctx.send(embed=send_error_msg("Error: Help Page Not Found",page_error_text))
            return
        commands_dict = get_commands(curr_page) #Pulls command list for current page of menu
        caller = ctx.message.author
        # Determine which help pages the user can access based on their role
        if validate_role(caller,"Mods") or validate_role(caller,"Dev"):
            max_page=8
        elif validate_role(caller,"Interns"):
            max_page=6
        elif validate_role(caller,"Tenants"):
            max_page=4
        else:
            max_page=1
        if curr_page > max_page:
            await ctx.send(embed=send_error_msg("Error: Invalid Permissions",no_permission))
            return
        #Sets up the help menu as a fancy embed for formatting
        embed=discord.Embed(title="",description=help_descr_text, color=help_orange)
        embed.set_author(name="Help Menu", icon_url=help_icon)
        for key in commands_dict: #Display commands (special icons for newly added ones)
            if key[:3] == "NEW":
                embed.add_field(name=help_new_emoji+" c!"+key[3:].replace('_',' '),
                value=commands_dict[key]+"\n-",inline=False)
            else:
                embed.add_field(name=help_diamond_emoji+" c!"+key.replace('_',' '),
                value=commands_dict[key]+"\n-",inline=False)
        embed.set_footer(text=help_footer+"| Current Page "+str(curr_page)+"/"+str(max_page))
        help = await ctx.send(embed=embed)
        # Grab the valid pages based on previous role check and max page
        valid_pages = [emoji_numbers[ind] for ind in range(max_page)]
        for emoji in valid_pages: #Add the 'menu pages' as reactions
            await help.add_reaction(emoji)
        while 1:
            try:
                #Wait for user to react to the menu and store user info and reaction
                reaction, user = await bot.wait_for('reaction_add',timeout=10)
                react_author = user.name+"#"+user.discriminator
                if (react_author == str(caller)) and (reaction.emoji in emoji_numbers): #only the user who asked for help can change the page
                    # Update the embed to have proper commands shown
                    curr_page = emoji_numbers.index(reaction.emoji) + 1
                    if curr_page <= max_page: # Ensures the user can't access confusing pages
                        commands_dict = get_commands(curr_page)
                        #print ("Bot should change to page " + str(curr_page) + " for user " +user.name) # Debug statement
                        embed=discord.Embed(title="",description=help_descr_text, color=help_orange)
                        embed.set_author(name="Help Menu", icon_url=help_icon)
                        for key in commands_dict:
                            if key[:3] == "NEW":
                                embed.add_field(name=help_new_emoji+" c!"+key[3:].replace('_',' '),
                                value=commands_dict[key]+"\n-",inline=False)
                            else:
                                embed.add_field(name=help_diamond_emoji+" c!"+key.replace('_',' '),
                                value=commands_dict[key]+"\n-",inline=False)
                        embed.set_footer(text=help_footer+"| Current Page "+str(curr_page)+"/"+str(max_page))
                        await help.edit(embed=embed) #Actually updates the embed
                        await help.remove_reaction(reaction,user) #Removes user reaction for easier page changing
            except: #Most likely Timeout Error Waiting for a reaction
                #Update footer so user knows they can no longer change page and takes away buttons
                embed.set_footer(text=help_footer_done+"| Current Page "+str(curr_page)+"/"+str(max_page))
                await help.edit(embed=embed)
                await help.clear_reactions()
                return
    else: #If Maintenance
        await ctx.send(embed=send_maintenance_msg())

# TENANT COMMAND PAGE 1 COMMAND 2
@commands.has_any_role("Ghosts","Tenants","Interns","Mods","Dev")
@bot.command(name='tenant',ignore_extra=False)#rolls random tenant and display info (from full list or event list)
async def critter_tenant(ctx):
    global maintenance #maintenance check
    if maintenance:
        tenant_pulled_list = read_sheets(CRITTER_CONFIG_ID,TENANT_LIST)
        chosen = random.choice(tenant_pulled_list)
        embed=discord.Embed(title="",description=(tenant_text % (chosen[0],chosen[3])),color=generic_blue)
        embed.set_author(name="Random Tenant",icon_url=tenant_icon)
        embed.set_image(url=chosen[2])
        await ctx.send(embed=embed)
    else:
        await ctx.send(embed=send_maintenance_msg())

# JOIN COMMAND PAGE 1 COMMAND 3
@commands.has_any_role("Ghosts","Tenants","Interns","Mods","Dev")
@bot.command(name='join',ignore_extra=False) #User adds themselves to role specified (in google sheet)
async def critter_join(ctx,*,role_name):
    global maintenance #maintenance check
    if maintenance:
        global guild
        #Pull role information from the Critter Sheet
        role_info = read_sheets(CRITTER_CONFIG_ID,ROLES_LOC)
        role_names = []
        role_ids = []
        need_member = []
        roles_to_join = []
        role_name_list = [elem.strip().lower().replace('"','').replace("'",'') for elem in role_name.split(",")]
        for entry in role_info: #Separate the role names, ids, and booleans
            role_names.append(entry[0])
            role_ids.append(entry[1])
            need_member.append(entry[2])
        test_role_names = [roles.lower() for roles in role_names]
        for role_name in role_name_list:
            if role_name.lower() not in test_role_names: #Check to ensure we are looking for a valid role
                await ctx.send(embed=send_error_msg("Error: Role Not Found",unknown_role_name))
                return
            else: #If we have a valid role, add the official name to the list
                role_id = test_role_names.index(role_name.lower())
                roles_to_join.append(discord.utils.get(bot.guilds[guild_index].roles, name=role_names[role_id]))
        #Check to ensure the user has the permissions to update target roles
        user = ctx.message.author
        if validate_role(user,'Tenants') or validate_role(user,'Interns') or validate_role(user,'Mods'):
            # User has rights to any role
            roles_joined = []
            roles_unjoined = []
            for role_to_join in roles_to_join:
                if validate_role(user,role_to_join.name): #If you already have the role, list sepatately
                    roles_unjoined.append(str(role_to_join.name))
                else: #If you don't have the role, list and add it
                    roles_joined.append(str(role_to_join.name))
                    await ctx.message.author.add_roles(role_to_join)
            roles_string = stringify_list(roles_joined) #roles you joined as a str
            unjoined_string = stringify_list(roles_unjoined) #roles you already had as a str
            if roles_string: #If you successfully joined at least one role
                join_message = (join_text % roles_string) #message for joining roles
                if unjoined_string: #If you tried to join a role you had
                    join_message += "\n\n"+(unjoin_text % unjoined_string) #message for previous roles
                join_embed = discord.Embed(title="",description=join_message,color=success_green)
                join_embed.set_author(name="Role(s) Joined Successfully", icon_url=check_grn_icon)
            else: #Only entered roles you alredy had gets different message
                join_embed = discord.Embed(title="",description=(unjoin_text % unjoined_string),color=success_green)
                join_embed.set_author(name="You're Already Assigned to These Roles(s)", icon_url=check_grn_icon)
            await ctx.send(embed=join_embed)
        else:
            # User does not have rights to any restricted roles
            for role_name in role_name_list:
                if ((need_member[test_role_names.index(role_name)]).lower() != "false"):
                    await ctx.send(embed=send_error_msg("Error: Invalid Permissions",no_permission))
                    return
            # Unrestricted roles are still safe
            roles_joined = []
            roles_unjoined = []
            for role_to_join in roles_to_join:
                if validate_role(user,role_to_join.name): #If you already have the role, list sepatately
                    roles_unjoined.append(str(role_to_join.name))
                else: #If you don't have the role, list and add it
                    roles_joined.append(str(role_to_join.name))
                    await ctx.message.author.add_roles(role_to_join)
            roles_string = stringify_list(roles_joined) #roles you joined as a str
            unjoined_string = stringify_list(roles_unjoined) #roles you already had as a str
            if roles_string: #If you successfully joined at least one role
                join_message = (join_text % roles_string) #message for joining roles
                if unjoined_string: #If you tried to join a role you had
                    join_message += "\n\n"+(unjoin_text % unjoined_string) #message for previous roles
                join_embed = discord.Embed(title="",description=join_message,color=success_green)
                join_embed.set_author(name="Role(s) Joined Successfully", icon_url=check_grn_icon)
            else: #Only entered roles you alredy had gets different message
                join_embed = discord.Embed(title="",description=(unjoin_text % unjoined_string),color=success_green)
                join_embed.set_author(name="You're Already Assigned to These Roles(s)", icon_url=check_grn_icon)
            await ctx.send(embed=join_embed)
    else:
        await ctx.send(embed=send_maintenance_msg())

# LEAVE COMMAND PAGE 1 COMMAND 4
@commands.has_any_role("Ghosts","Tenants","Interns","Mods","Dev")
@bot.command(name='leave',ignore_extra=False) #User removes themselves from role specified (in google sheet)
async def critter_leave(ctx,*,role_name):
    global maintenance #maintenance check
    if maintenance:
        global guild
        #Pull role information from the Critter Sheet
        role_info = read_sheets(CRITTER_CONFIG_ID,ROLES_LOC)
        role_names = []
        role_ids = []
        need_member = []
        roles_to_leave = []
        role_name_list = [elem.strip().lower().replace('"','').replace("'",'') for elem in role_name.split(",")]
        for entry in role_info: #Separate the role names, ids, and booleans
            role_names.append(entry[0])
            role_ids.append(entry[1])
            need_member.append(entry[2])
        test_role_names = [roles.lower() for roles in role_names]
        for role_name in role_name_list:
            if role_name.lower() not in test_role_names: #Check to ensure we are looking for a valid role
                await ctx.send(embed=send_error_msg("Error: Role Not Found",unknown_role_name))
                return
            else:
                role_id = test_role_names.index(role_name.lower())
                roles_to_leave.append(discord.utils.get(bot.guilds[guild_index].roles, name=role_names[role_id]))
        #Check to ensure the user has the permissions to update target roles
        user = ctx.message.author
        for role_to_leave in roles_to_leave:
            if not validate_role(user,role_to_leave): #Check the user has the role they wish to leave
                await ctx.send(embed=send_error_msg("Error: Can't Lose What You Don't Have",no_role % role_to_leave))
                return
        if validate_role(user,'Tenants') or validate_role(user,'Interns') or validate_role(user,'Mods'):
            # User has rights to any role
            for role_to_leave in roles_to_leave:
                await ctx.message.author.remove_roles(role_to_leave)
            roles_left = [str(role.name) for role in roles_to_leave]
            roles_string = stringify_list(roles_left)
            leave_embed = discord.Embed(title="",description=(leave_text % roles_string),color=success_green)
            leave_embed.set_author(name="Role(s) Left Successfully", icon_url=check_grn_icon)
            await ctx.send(embed=leave_embed)
        else:
            # User does not have rights to any restricted roles
            for role_name in role_name_list:
                if ((need_member[test_role_names.index(role_name)]).lower() != "false"):
                    await ctx.send(embed=send_error_msg("Error: Invalid Permissions",no_permission))
                    return
            # Unrestricted roles are still safe
            for role_to_leave in roles_to_leave:
                await ctx.message.author.remove_roles(role_to_leave)
            roles_left = [str(role.name) for role in roles_to_leave]
            roles_string = stringify_list(roles_left)
            leave_embed = discord.Embed(title="",description=(leave_text % roles_string),color=success_green)
            leave_embed.set_author(name="Role(s) Left Successfully", icon_url=check_grn_icon)
            await ctx.send(embed=leave_embed)
    else:
        await ctx.send(embed=send_maintenance_msg())

# PING COMMAND PAGE 1 COMMAND 5
@commands.has_any_role("Ghosts","Tenants","Interns","Mods","Dev")
@bot.command(name='ping',ignore_extra=False) #Pings the bot to check response time
async def critter_ping(ctx):
    global maintenance #maintenance check
    if maintenance:
        pong_embed=discord.Embed(title="",description=("Checking %s's latency" % BOTNAME), color=paddle_red)
        pong_embed.set_author(name="Pong", icon_url=pong_icon)
        ping_pong = await ctx.send(embed=pong_embed) # Start by letting the user know its a latency check in case of issues
        pong_embed=discord.Embed(title="",description=('Pong! {0}ms'.format(round(bot.latency*1000))), color=paddle_red)
        pong_embed.set_author(name="Ping", icon_url=pong_icon)
        pong_embed.set_thumbnail(url=pong_image) # Cats play ping pong
        await ping_pong.edit(embed=pong_embed) # Update the embed
    else:
        await ctx.send(embed=send_maintenance_msg())

# INVENTORY COMMANDS PAGE 2 COMMAND 1, PAGE 7 COMMANDS 1,2 and 3
@commands.has_any_role("Tenants","Interns","Mods","Dev")
@bot.command(name='inventory',ignore_extra=False) #shows user inventory or allows mods to link/view/update inventory info in the bot
async def critter_inventory(ctx,command_ext='NULL',user='NULL',database_tab_name='NULL'):
    global maintenance #maintenance check
    error = False
    if maintenance:
        # Update the user inventory mapping by pulling sheets user data
        users_info = read_sheets(CRITTER_CONFIG_ID,USER_INFO_LOC)
        # Convert 2d Lists into 1d Lists (just pulled column data)
        user_full_names = [user[0] for user in users_info]
        user_inv_names = [user[1] for user in users_info]
        # Combines this into dictionary
        user_inventory_map = dict(zip(user_full_names,user_inv_names))
        if command_ext == 'NULL': #Default case, Displays inventory (update w/sheets functionality)
            user = str(ctx.message.author)
            if user in user_inventory_map: #If the user has an inventory
                tab_name =  user_inventory_map[user] #Find the tab
                #Load user inventory from sheets
                user_inventory = read_sheets(SERVER_INVENTORY_DB,tab_name+INVENTORY_LOC)
                if not user_inventory:
                    embed=discord.Embed(title="",description=empty_inventory,color=help_orange)
                    embed.set_author(name=("%s's Inventory" % tab_name), icon_url=inventory_icon)
                    inventory = await ctx.send(embed=embed)
                    return
                items_per_page = 10
                max_page = math.ceil(len(user_inventory)/items_per_page)
                curr_page = 0
                #Display inventory contents
                inv_string = "" #Build inventory as 1 blocky string
                for item_ind in range(items_per_page): #Add each item to the block
                    ind = (curr_page)*items_per_page+item_ind
                    if ind >= len(user_inventory):
                        break
                    #Format them one at a time
                    if len(user_inventory[ind][0]) > 24:
                        user_inventory[ind][0] = (user_inventory[ind][0][:21]+"...")
                    if user_inventory[ind][0].lower().strip() == "summoning for dummies":
                        user_inventory[ind][0] = ('ʺ'+user_inventory[ind][0]+'ʺ').replace('for','fo​r')
                        inv_string += '║ {:25s} ║ {:10s} ║\n'.format(user_inventory[ind][0].replace("'",'ʼ'),user_inventory[ind][1])
                    else:
                        inv_string += '║ {:24s} ║ {:10s} ║\n'.format(user_inventory[ind][0].replace("'",'ʼ'),user_inventory[ind][1])
                        #Check if this is the last one
                    if ind != (len(user_inventory) - 1) and item_ind != items_per_page-1:
                        #If not, add a "line break"
                        inv_string += table_linebreak+"\n"
                inv_string += table_ender #Close out the inventory block
                # Stuff it in an embed and output it to the user
                embed=discord.Embed(title="",description=("```bash\n%s\n%s```" % (inventory_header,inv_string)),color=help_orange)
                embed.set_author(name=("%s's Inventory" % tab_name), icon_url=inventory_icon)
                embed.set_footer(text=(table_footer % (curr_page+1,max_page)))
                inventory = await ctx.send(embed=embed)
                valid_pages = [emoji_numbers[ind] for ind in range(max_page)]
                for emoji in valid_pages: #Add the 'menu pages' as reactions
                    await inventory.add_reaction(emoji)
                while 1:
                    try:
                        #Wait for user to react to the menu and store user info and reaction
                        reaction, reactor = await bot.wait_for('reaction_add',timeout=10)
                        react_author = reactor.name+"#"+reactor.discriminator
                        if (react_author == str(user)) and (reaction.emoji in valid_pages):
                            #only the user who asked for inventory can access page
                            curr_page = valid_pages.index(reaction.emoji)
                            inv_string = "" #Build inventory as 1 blocky string
                            for item_ind in range(items_per_page): #Add each item to the block
                                ind = (curr_page)*items_per_page+item_ind
                                if ind >= len(user_inventory):
                                    break
                                #Format them one at a time
                                if len(user_inventory[ind][0]) > 24:
                                    user_inventory[ind][0] = (user_inventory[ind][0][:21]+"...")
                                if user_inventory[ind][0].lower().strip() == "summoning for dummies":
                                    user_inventory[ind][0] = ('ʺ'+user_inventory[ind][0]+'ʺ').replace('for','fo​r')
                                    inv_string += '║ {:25s} ║ {:10s} ║\n'.format(user_inventory[ind][0].replace("'",'ʼ'),user_inventory[ind][1])
                                else:
                                    inv_string += '║ {:24s} ║ {:10s} ║\n'.format(user_inventory[ind][0].replace("'",'ʼ'),user_inventory[ind][1])
                                #Check if this is the last one
                                if ind != (len(user_inventory) - 1) and item_ind != items_per_page-1:
                                    #If not, add a "line break"
                                    inv_string += table_linebreak+"\n"
                            inv_string += table_ender #Close out the inventory block
                            # Stuff it in an embed and output it to the user
                            embed=discord.Embed(title="",description=("```bash\n%s\n%s```" % (inventory_header,inv_string)),color=help_orange)
                            embed.set_author(name=("%s's Inventory" % tab_name), icon_url=inventory_icon)
                            embed.set_footer(text=(table_footer % (curr_page+1,max_page)))
                            await inventory.edit(embed=embed) #Actually updates the embed
                            await inventory.remove_reaction(reaction,reactor) #Removes user reaction for easier page changing
                    except: #Most likely Timeout Error Waiting for a reaction
                        #Update footer so user knows they can no longer change page and takes away buttons
                        embed.set_footer(text=inventory_footer_done% (curr_page+1,max_page))
                        await inventory.edit(embed=embed)
                        await inventory.clear_reactions()
                        return
            else:
                await ctx.send(embed=send_error_msg("Error: Member Database Error",(no_inventory_tab % user.split('#')[0])))
                return
        else:
            if validate_role(ctx.message.author,"Mods") or validate_role(ctx.message.author,"Dev"):
                if command_ext.lower() == 'add': # Add a link to local storage
                    if user == 'NULL' or database_tab_name == 'NULL': # Argument verification
                        arg_txt = "username or database tab name"
                        await ctx.send(embed=send_error_msg("Error: Missing Argument",(missed_argument % arg_txt)))
                        return
                    # Validate the specified tab name
                    member_db_tabs = tab_list_sheets(SERVER_INVENTORY_DB)
                    inventory_directory = Diff(member_db_tabs,non_member_tabs)
                    # Grab the official tab name/check for match (this way is case insensitive)
                    tab_name = [entry for entry in inventory_directory if entry.lower() == database_tab_name.lower()]
                    if not tab_name: # If there was no match in the directory
                        await ctx.send(embed=send_error_msg("Error: I Can't Find That Tab Name",(invalid_tab_name % database_tab_name)))
                        error = True
                    # Argument contains valid tab name
                    try:
                        arg_user_name = str(await bot.fetch_user(user[2:-1].replace("!",'')))
                    except:
                        await ctx.send(embed=send_error_msg("Error: Unknown User",unknown_user))
                        return
                    if not arg_user_name in user_inventory_map: # Add non-existent user to the map
                        if error:
                            return
                        inv_embed = discord.Embed(title="",description=(inventory_add_text % (tab_name[0],user)),color=success_green)
                        inv_embed.set_author(name="Added Inventory Tab", icon_url=check_grn_icon)
                        await ctx.send(embed = inv_embed)
                        users_info.append([arg_user_name, tab_name[0], 0])
                    else: # Already have this user
                        await ctx.send(embed=send_error_msg("Error: User Already In DB",(yes_inventory_tab % user)))
                        return
                elif command_ext.lower() == 'update': # Update a link in local storage
                    if user == 'NULL' or database_tab_name == 'NULL': # Argument verification
                        arg_txt = "username or database tab name"
                        await ctx.send(embed=send_error_msg("Error: Missing Argument",(missed_argument % arg_txt)))
                        return
                    # Validate the specified tab name
                    member_db_tabs = tab_list_sheets(SERVER_INVENTORY_DB)
                    inventory_directory = Diff(member_db_tabs,non_member_tabs)
                    # Grab the official tab name/check for match (this way is case insensitive)
                    tab_name = [entry for entry in inventory_directory if entry.lower() == database_tab_name.lower()]
                    if not tab_name: # If there was no match in the directory
                        await ctx.send(embed=send_error_msg("Error: I Can't Find That Tab Name",(invalid_tab_name % database_tab_name)))
                        error = True
                    # Argument contains valid tab name
                    try:
                        arg_user_name = str(await bot.fetch_user(user[2:-1].replace("!",'')))
                    except:
                        await ctx.send(embed=send_error_msg("Error: Unknown User",unknown_user))
                        return
                    if arg_user_name in user_inventory_map: # If the user exists in the mapping
                        if error:
                            return
                        inv_embed = discord.Embed(title="",description=(inventory_update_text % (user,user_inventory_map[arg_user_name],tab_name[0])),color=success_green)
                        inv_embed.set_author(name="Updated Inventory Tab", icon_url=check_grn_icon)
                        await ctx.send(embed = inv_embed)
                        users_info[user_full_names.index(arg_user_name)][1] = tab_name[0]
                    else: #Invalid user (not in the mapping)
                        await ctx.send(embed=send_error_msg("Error: Member Database Error",(no_inventory_tab % arg_user_name.split('#')[0])))
                        return
                elif command_ext.lower() == 'view': # View the link in local storage
                    if database_tab_name != "NULL":
                        await ctx.send(embed=send_error_msg("Error: Bamboozled",too_many_args))
                        return
                    if user == 'NULL': #Argument verification
                        arg_txt = "username"
                        await ctx.send(embed=send_error_msg("Error: Missing Argument",(missed_argument % arg_txt)))
                        return
                    try:
                        arg_user_name = str(await bot.fetch_user(user[2:-1].replace("!",'')))
                    except:
                        await ctx.send(embed=send_error_msg("Error: Unknown User",unknown_user))
                        return
                    if arg_user_name in user_inventory_map: #If the user exists in the mapping
                        # Display the mapping
                        inv_embed = discord.Embed(title="",description=(inventory_view_text % (user,user_inventory_map[arg_user_name])),color=success_green)
                        inv_embed.set_author(name="Inventory Tab Name", icon_url=check_grn_icon)
                        await ctx.send(embed = inv_embed)
                        return
                    else: #Invalid user (not in the mapping)
                        await ctx.send(embed=send_error_msg("Error: Member Database Error",(no_inventory_tab % arg_user_name.split('#')[0])))
                        return
                else:
                    await ctx.send(embed=send_error_msg("Error: Command Error",invalid_command))
                    return
                write_sheets(CRITTER_CONFIG_ID,USER_INFO_LOC,users_info,2)
            else:
                await ctx.send(embed=send_error_msg("Error: Invalid Permissions",no_permission))
                return
    else:
        await ctx.send(embed=send_maintenance_msg())

# BALANCE COMMANDS PAGE 2 COMMAND 2 and 3
@commands.has_any_role("Tenants","Interns","Mods","Dev")
@bot.command(name='balance',ignore_extra=False) #Shows user balance or global leaderboards of $
async def critter_balance(ctx,command_ext='NULL'):
    global maintenance #maintenance check
    if maintenance:
        # Update the user inventory mapping by pulling sheets user data
        users_info = read_sheets(CRITTER_CONFIG_ID,USER_INFO_LOC)
        # Convert 2d Lists into 1d Lists (just pulled column data)
        user_full_names = [user[0] for user in users_info]
        user_inv_names = [user[1] for user in users_info]
        # Combines this into dictionary
        user_inventory_map = dict(zip(user_full_names,user_inv_names))
        if command_ext == 'NULL': #Default case is user's balance
            user = str(ctx.message.author)
            if user in user_inventory_map: #verify user is in the inventory map
                tab_name =  user_inventory_map[user] #grab inventory tab name
                # Load PD and shard balances from user inventory tab
                pd_balance = read_sheets(SERVER_INVENTORY_DB,tab_name+PD_BAL_LOC)[0]
                shard_balance = read_sheets(SERVER_INVENTORY_DB,tab_name+SHARD_BAL_LOC)[0]
                # Display information to user
                balance_embed=discord.Embed(title="",description=(balance_text % (pd_balance[0],shard_balance[0])),color=pika_yellow)
                balance_embed.set_author(name=("%s's Balance" % tab_name),icon_url=balance_icon)
                await ctx.send(embed=balance_embed)
            else:
                await ctx.send(embed=send_error_msg("Error: Member Database Error",(no_inventory_tab % user.split('#')[0])))
        elif command_ext.lower() == 'top': #Top indicates we want leaderboards
            balance_top = {} #Establish dict for balances
            # Load in all the inventory tab names
            member_db_tabs = tab_list_sheets(SERVER_INVENTORY_DB)
            inventory_directory = Diff(member_db_tabs,non_member_tabs)
            # Establish list of ranges to read
            range_list = [tab_name.strip()+PD_BAL_LOC for tab_name in inventory_directory]
            # Grab all balances across all inventories
            bal_list = read_sheets_multiple(SERVER_INVENTORY_DB,range_list)
            for ind in range(len(inventory_directory)): # For each user with an
            #inventory tab, add their balance to the dictionary
                balance_top[inventory_directory[ind]] = int(bal_list[ind][0])
            #load in critter's balance
            critter_balance_var = read_sheets(SERVER_INVENTORY_DB,CRITTER_BALANCE_LOC)[0]
            critter_balance_var = int(critter_balance_var[0])
            #add critter's balance to "balance top" array
            balance_top[BOTNAME] = critter_balance_var
            # Sort the balance dict based on the values
            sorted_balance = sorted(balance_top.items(), key = lambda kv:kv[1],reverse=True)
            balance_embed=discord.Embed(title="",description="",color=pika_yellow)
            balance_embed.set_author(name="Richest Members",icon_url=balance_icon)
            leaders = "-------------\n"
            for ind in range(3):
                leaders += (balance_leader % (balance_emoji_medals[ind],sorted_balance[ind][0],sorted_balance[ind][1]))
            balance_embed.add_field(name=balance_top_start,value=leaders,inline=False)
            runner_ups = "---------------\n"
            for ind in range(2):
                runner_ups += (balance_leader % (hm_star_emoji,sorted_balance[ind+3][0],sorted_balance[ind+3][1]))
            balance_embed.add_field(name="​",value="**"+balance_mention_start+"**\n"+runner_ups,inline=False)
            await ctx.send(embed=balance_embed)
        elif command_ext.lower() == 'critter': #Critter indicates we want critter
            #load in critter's balance
            critter_balance_var = read_sheets(SERVER_INVENTORY_DB,CRITTER_BALANCE_LOC)[0]
            critter_balance_var = int(critter_balance_var[0])
            balance_embed=discord.Embed(title="",description=(critter_balance_text % critter_balance_var),color=pika_yellow)
            balance_embed.set_author(name="Critter's Balance",icon_url=balance_icon)
            await ctx.send(embed=balance_embed) #display critter's balance
        else:
            await ctx.send(embed=send_error_msg("Error: Command Error",invalid_command))
    else:
        await ctx.send(embed=send_maintenance_msg())

# SHOP COMMANDS PAGE 2 COMMANDS 4 and 5
@commands.has_any_role("Tenants","Interns","Mods","Dev")
@bot.command(name='shop',ignore_extra=False) #Bot displays the shop page specified
async def critter_shop(ctx,page_num='0'): #Default case is menu that shows pages
    global maintenance #maintenance check
    if maintenance:
        users_info = read_sheets(CRITTER_CONFIG_ID,USER_INFO_LOC)
        # Convert 2d Lists into 1d Lists (just pulled column data)
        user_full_names = [user[0] for user in users_info]
        user_key_total = [user[2] for user in users_info]
        key_num = read_sheets(CRITTER_CONFIG_ID,KEY_PRICE_INC_LOC)[0]
        key_num = key_num[0]
        user = str(ctx.message.author)
        if not page_num.isdigit():
            await ctx.send(embed=send_error_msg("Error: Shop Page Not Found",page_error_text))
            return
        curr_page = int(page_num)
        max_page = 8
        if(curr_page):
            if shop_page_decode(curr_page) == -1:
                await ctx.send(embed=send_error_msg("Error: Shop Page Not Found",page_error_text))
                return
            shop_data = read_sheets(CRITTER_CONFIG_ID,shop_page_decode(curr_page))[1:]
            #Display inventory contents
            shop_string = "" #Build inventory as 1 blocky string
            for item in shop_data: #Add each item to the block
                if item[1].strip() == "--":
                    ind = 2
                else:
                    ind = 1
                #Format them one at a time
                if len(item[0]) > 24:
                    item[0] = (item[0][:21]+"...")
                if item[0].lower().strip() == key_name:
                    key_add = int(key_num)*int(user_key_total[user_full_names.index(user)])
                    item[1] = str(int(item[1])+key_add)
                if item[0].lower().strip() == "summoning for dummies":
                    item[0] = ('ʺ'+item[0]+'ʺ').replace('for','fo​r')
                    shop_string += '║ {:25s} ║ {:14s} ║\n'.format(item[0].replace("'",'ʼ'),item[ind])
                else:
                    shop_string += '║ {:24s} ║ {:14s} ║\n'.format(item[0].replace("'",'ʼ'),item[ind])
                    #Check if this is the last one
                if shop_data.index(item) != (len(shop_data) - 1):
                    #If not, add a "line break"
                    shop_string += shop_linebreak+"\n"
            shop_string += shop_ender #Close out the inventory block
            # Stuff it in an embed and output it to the user
            if shop_data[0][1].strip() == "--":
                embed=discord.Embed(title=shop_titles[curr_page-1],description=("```bash\n%s\n%s```" % (shop_header_shards,shop_string)),color=function_pink)
            else:
                embed=discord.Embed(title=shop_titles[curr_page-1],description=("```bash\n%s\n%s```" % (shop_header_PD,shop_string)),color=function_pink)
            embed.set_author(name="Critter Shop", icon_url=shop_icon)
        else:
            #Needs a lot of formatting work probably an embed
            embed=discord.Embed(title="Shop Menu",description=(shop_menu_text),color=function_pink)
            embed.set_author(name=("Critter Shop"), icon_url=shop_icon)
            for ind in range(max_page):
                embed.add_field(name=("| Page %s" % str(ind+1)),value=shop_titles[ind],inline=False)
        embed.set_footer(text=(table_footer % (curr_page,max_page)))
        shop = await ctx.send(embed=embed)
        valid_pages = [shop_emoji_numbers[ind] for ind in range(max_page+1)]
        for emoji in valid_pages: #Add the 'menu pages' as reactions
            await shop.add_reaction(emoji)
        while 1:
            try:
                #Wait for user to react to the menu and store user info and reaction
                reaction, reactor = await bot.wait_for('reaction_add',timeout=10)
                react_author = reactor.name+"#"+reactor.discriminator
                if (react_author == str(user)) and (reaction.emoji in valid_pages):
                    #only the user who asked for inventory can access page
                    curr_page = valid_pages.index(reaction.emoji)
                    if curr_page:
                        shop_data = read_sheets(CRITTER_CONFIG_ID,shop_page_decode(curr_page))[1:]
                        shop_string = "" #Build inventory as 1 blocky string
                        for item in shop_data: #Add each item to the block
                            if item[1].strip() == "--":
                                ind = 2
                            else:
                                ind = 1
                            #Format them one at a time
                            if len(item[0]) > 24:
                                item[0] = (item[0][:21]+"...")
                            if item[0].lower().strip() == key_name:
                                key_add = int(key_num)*int(user_key_total[user_full_names.index(user)])
                                item[1] = str(int(item[1])+key_add)
                            if item[0].lower().strip() == "summoning for dummies":
                                item[0] = ('ʺ'+item[0]+'ʺ').replace('for','fo​r')
                                shop_string += '║ {:25s} ║ {:14s} ║\n'.format(item[0].replace("'",'ʼ'),item[ind])
                            else:
                                shop_string += '║ {:24s} ║ {:14s} ║\n'.format(item[0].replace("'",'ʼ'),item[ind])
                                #Check if this is the last one
                            if shop_data.index(item) != (len(shop_data) - 1):
                                #If not, add a "line break"
                                shop_string += shop_linebreak+"\n"
                        shop_string += shop_ender #Close out the inventory block
                        # Stuff it in an embed and output it to the user
                        if shop_data[0][1].strip() == "--":
                            embed=discord.Embed(title=shop_titles[curr_page-1],description=("```bash\n%s\n%s```" % (shop_header_shards,shop_string)),color=function_pink)
                        else:
                            embed=discord.Embed(title=shop_titles[curr_page-1],description=("```bash\n%s\n%s```" % (shop_header_PD,shop_string)),color=function_pink)
                        embed.set_author(name="Critter Shop", icon_url=shop_icon)
                    else:
                        #Needs a lot of formatting work probably an embed
                        embed=discord.Embed(title="Shop Menu",description=(shop_menu_text),color=function_pink)
                        embed.set_author(name=("Critter Shop"), icon_url=shop_icon)
                        for ind in range(max_page):
                            embed.add_field(name=("| Page %s" % str(ind+1)),value=shop_titles[ind],inline=False)
                    embed.set_footer(text=(table_footer % (curr_page,max_page)))
                    await shop.edit(embed=embed) #Actually updates the embed
                    await shop.remove_reaction(reaction,reactor) #Removes user reaction for easier page changing
            except: #Most likely Timeout Error Waiting for a reaction
                #Update footer so user knows they can no longer change page and takes away buttons
                embed.set_footer(text=(shop_footer_done % (curr_page,max_page)))
                await shop.edit(embed=embed)
                await shop.clear_reactions()
                return
    else:
        await ctx.send(embed=send_maintenance_msg())

# BUY COMMAND PAGE 3 COMMAND 1
@commands.has_any_role("Tenants","Interns","Mods","Dev")
@bot.command(name='buy',ignore_extra=False) #Bot buys the specified quantity of specified item
async def critter_buy(ctx,item,quantity):
    global maintenance #maintenance check
    error = False
    if maintenance:
        if quantity.isdigit(): # Need Number for quantity
            if int(quantity) <= 0: # Number has to be positive
                await ctx.send(embed=send_error_msg("Error: Invalid Number of Items",inv_quantity_text))
                error = True
        else:
            await ctx.send(embed=send_error_msg("Error: Invalid Number of Items",inv_quantity_text))
            # Invalid quantity (not positive number)
            error = True
        item_off_name = "" # Initialize the Official Item Name
        # Load in all items from the shop
        all_items = read_sheets_multiple(CRITTER_CONFIG_ID,ALL_ITEMS_LOC)
        for shop_item in all_items: # Go through the items one by one
            if shop_item[0].lower() == item.lower().replace("’","'"): # Check for a match with argument
                item_off_name = shop_item[0] #Grab official name
                pd_price = shop_item[1].strip() #Grab price in pd
                shard_price = shop_item[2].strip() #Grab price in shards
        if not item_off_name: # If we didn't match there's no official name
            # Error, invalid item
            await ctx.send(embed=send_error_msg("Error: Unbuyable Item",(invalid_shop_item % ("buy",item))))
            error = True
        #print(item_off_name,pd_price,shard_price) good for debugging
        # Update the user inventory mapping by pulling sheets user data
        users_info = read_sheets(CRITTER_CONFIG_ID,USER_INFO_LOC)
        # Convert 2d Lists into 1d Lists (just pulled column data)
        user_full_names = [user[0] for user in users_info]
        user_inv_names = [user[1] for user in users_info]
        user_key_total = [user[2] for user in users_info]
        # Combines this into dictionary
        user_inventory_map = dict(zip(user_full_names,user_inv_names))
        # Load in the price increase per key
        key_num = read_sheets(CRITTER_CONFIG_ID,KEY_PRICE_INC_LOC)[0]
        key_num = key_num[0]
        user = str(ctx.message.author) # Grab user info for inventory compare
        if error:
            return
        if user in user_inventory_map: #verify user is in the inventory map
            tab_name =  user_inventory_map[user] #grab inventory tab name
            user_inventory = read_sheets(SERVER_INVENTORY_DB,tab_name+INVENTORY_LOC)
            # read in the user inventory
            if pd_price != "--": # If the item costs pd
                # Grab user's pd balance and calculate cost
                pd_balance = read_sheets(SERVER_INVENTORY_DB,tab_name+PD_BAL_LOC)[0]
                pd_balance = pd_balance[0]
                if item_off_name.lower() == key_name: #If the user is buying a key
                # Compute the total price of keys to buy
                # Key price = BP + INC * #Owned per key (buying many at once makes it weird)
                # BP = 3000 (base price), INC = 1500 (incremental cost)
                # Total key price = KP * Quantity + INC * Tri(Quantity - 1)
                # Tri(n) = (n^2+n)/2 pretty sure that works out right
                    key_add = int(key_num)*int(user_key_total[user_full_names.index(user)])
                    base_price = int(pd_price)+key_add
                    pd_cost = base_price*int(quantity)+triangle_num(int(quantity)-1)*int(key_num)
                else:
                    pd_cost = int(pd_price)*int(quantity)
                if int(pd_balance) >= pd_cost: # If the user can afford, buy
                    found = False
                    for entry in user_inventory: # Check if item in inventory
                        if entry[0].lower() == item.lower():
                            # If the item is in the inventory, update quantity
                            entry[1] = str(int(entry[1]) + int(quantity))
                            found = True
                            break
                    if not found: # If item not in inventory, add it
                        new_entry = [item_off_name,quantity]
                        user_inventory.append(new_entry)
                    pd_balance = int(pd_balance)-pd_cost # calculate new balance
                    # Write new balance and inventory to google sheet
                    write_sheets(SERVER_INVENTORY_DB,tab_name+PD_BAL_LOC,pd_balance,0)
                    if item_off_name.lower() == key_name: # Adding a key to inventory
                        # Have to add quantity keys to user's key total
                        num_keys = int(user_key_total[user_full_names.index(user)])
                        num_keys += int(quantity)
                        users_info[user_full_names.index(user)][2] = num_keys
                        write_sheets(CRITTER_CONFIG_ID,USER_INFO_LOC,users_info)
                    buy_embed=discord.Embed(title="",description=(buy_success_text_pd % (quantity,item_off_name,pd_cost)), color=buy_indigo)
                else:
                    await ctx.send(embed=send_error_msg("Error: Insufficient PD Funds",(no_money_text % (int(pd_balance),pd_cost-int(pd_balance)))))
                    # Error, can't affor buy
                    return
            if shard_price != "--": # If item costs shards
                # Grab user's shard balance and calculate cost
                shard_balance = read_sheets(SERVER_INVENTORY_DB,tab_name+SHARD_BAL_LOC)[0]
                shard_balance = shard_balance[0]
                shard_cost = int(shard_price)*int(quantity)
                if int(shard_balance) >= shard_cost: # If the user can afford, buy
                    found = False
                    for entry in user_inventory:
                        if entry[0].lower() == item.lower():
                            # If the item is in the inventory, update quantity
                            entry[1] = str(int(entry[1]) + int(quantity))
                            found = True
                            break
                    if not found: # If item not in inventory, add it
                        new_entry = [item_off_name,quantity]
                        user_inventory.append(new_entry)
                    shard_balance = int(shard_balance)-shard_cost # calculate new balance
                    buy_embed=discord.Embed(title="",description=(buy_success_text_shards % (quantity,item_off_name,shard_cost)), color=buy_indigo)
                    # Write new balance and inventory to google sheet
                    write_sheets(SERVER_INVENTORY_DB,tab_name+SHARD_BAL_LOC,shard_balance,0)
                else:
                    await ctx.send(embed=send_error_msg("Error: Insufficient Shard Funds",(no_shards_text % (int(shard_balance),shard_cost-int(shard_balance)))))
                    # Error, can't afford buy
                    return
            write_sheets(SERVER_INVENTORY_DB,tab_name+INVENTORY_LOC,user_inventory)
            buy_embed.set_author(name="Purchase Successful", icon_url=buy_icon)
            await ctx.send(embed=buy_embed)
            # Display information to user
        else:
            await ctx.send(embed=send_error_msg("Error: Member Database Error",(no_inventory_tab % user.split('#')[0])))
    else:
        await ctx.send(embed=send_maintenance_msg())

# SELL COMMAND PAGE 3 COMMAND 2
#Needs a lot of formatting work
@commands.has_any_role("Tenants","Interns","Mods","Dev")
@bot.command(name='sell',ignore_extra=False) #Bot buys the specified quantity of specified item
async def critter_sell(ctx,item,quantity):
    global maintenance #maintenance check
    error = False
    if maintenance:
        if quantity.isdigit(): # Need Number for quantity
            if int(quantity) <= 0: # Number has to be positive
                await ctx.send(embed=send_error_msg("Error: Invalid Number of Items",inv_quantity_text))
                error = True
        else:
            await ctx.send(embed=send_error_msg("Error: Invalid Number of Items",inv_quantity_text))
            # Invalid quantity (not positive number)
            error = True
        item_off_name = "" # Initialize the Official Item Name
        # Load in all items from the shop
        all_items = read_sheets_multiple(CRITTER_CONFIG_ID,ALL_ITEMS_LOC)
        # Update the user inventory mapping by pulling sheets user data
        users_info = read_sheets(CRITTER_CONFIG_ID,USER_INFO_LOC)
        # Convert 2d Lists into 1d Lists (just pulled column data)
        user_full_names = [user[0] for user in users_info]
        user_inv_names = [user[1] for user in users_info]
        # Combines this into dictionary
        user_inventory_map = dict(zip(user_full_names,user_inv_names))
        user = str(ctx.message.author) # Grab user info for inventory compare
        if error:
            return
        if user in user_inventory_map: #verify user is in the inventory map
            tab_name =  user_inventory_map[user] #grab inventory tab name
            user_inventory = read_sheets(SERVER_INVENTORY_DB,tab_name+INVENTORY_LOC)
            # read in the user inventory
            found = False
            possessed_quantity = 0
            for entry in user_inventory: # Check if item in inventory
                if entry[0].lower() == item.lower().replace("’","'"):
                    possessed_quantity = int(entry[1])
                    if possessed_quantity >= int(quantity):
                        # If the item is in the inventory, update quantity
                        entry[1] = str(int(entry[1]) - int(quantity))
                        found = True
                        if entry[1] == '0': # If the user no longer has any of the item
                            user_inventory.remove(entry) #remove it
                        break

            for shop_item in all_items: # Go through the items one by one
                if shop_item[0].lower() == item.lower().replace("’","'"): # Check for a match with argument
                    item_off_name = shop_item[0] #Grab official name
                    pd_price = shop_item[1].strip() #Grab price in pd
                    shard_price = shop_item[2].strip() #Grab price in shards
            if not item_off_name: # If we didn't match there's no official name
                # Load in the sell only items
                sell_only_items = read_sheets(CRITTER_CONFIG_ID,SELL_ITEMS_LOC)
                for sell_item in sell_only_items: # Check the sell-only items category
                    if sell_item[0].lower() == item.lower().replace("’","'"): # Check for a match with argument
                        item_off_name = sell_item[0] #Grab official name
                        pd_price = sell_item[1].strip() #Grab price in pd
                        shard_price = "--" #No shard price for these
                        break
                if not item_off_name: # Not in shop or "sell-only" items
                    trash_only_items = read_sheets(CRITTER_CONFIG_ID,TRASH_ITEMS_LOC)
                    if found and (item.lower() in [trash_item[0].lower() for trash_item in trash_only_items]):
                        # Output proposed action to user
                        embed=discord.Embed(title="",description=(item_delete_question %(quantity,item)), color=function_pink)
                        embed.set_author(name="Delete", icon_url=trash_icon)
                        sell = await ctx.send(embed=embed)
                        # Give the user option to confirm or reject
                        for emoji in emoji_confirm:
                            await sell.add_reaction(emoji)
                        while 1: # Needs to accept reactions until timeout or we see a valid reaction
                            try:
                                # Wait for user to react and store that info
                                reaction, reactor = await bot.wait_for('reaction_add',timeout=15)
                                react_author = reactor.name+"#"+reactor.discriminator
                                if (react_author == str(ctx.message.author)) and (reaction.emoji in emoji_confirm): #only the user who initiated can accept/cancel gift
                                    if reaction.emoji == emoji_confirm[0]: # User confirms delete
                                        # Write updated inventory to google sheet (clear it first to force update)
                                        clear_sheets(SERVER_INVENTORY_DB,tab_name+INVENTORY_LOC)
                                        write_sheets(SERVER_INVENTORY_DB,tab_name+INVENTORY_LOC,user_inventory)
                                        #Tells user what deleted and how many
                                        embed=discord.Embed(title="",description=(item_delete_confirm %(quantity,item)), color=success_green)
                                        embed.set_author(name="Delete", icon_url=check_grn_icon)
                                    else: # User cancels gift
                                        embed=discord.Embed(title="",description=(item_delete_reject % item), color=reject_red)
                                        embed.set_author(name="Delete", icon_url=check_red_icon)
                                    await sell.edit(embed=embed) #Actually updates the embed
                                    await sell.clear_reactions() #Clears reactions
                                    return # We only do this once
                            except: #should pretty much only happen in timeout
                                # Let user know that request timed out
                                embed=discord.Embed(title="",description=delete_timeout, color=reject_red)
                                embed.set_author(name="Delete", icon_url=error_icon)
                                await sell.edit(embed=embed) #Actually updates the embed
                                await sell.clear_reactions() #Clears reactions
                                return # Exit after timeout
                    else: # Not a trashable item
                        # Error, invalid item
                        await ctx.send(embed=send_error_msg("Error: Unsellable Item",(invalid_shop_item % ("sell",item))))
                        return
            if not found: # If item not in inventory error
                await ctx.send(embed=send_error_msg("Error: Lacking Item Quantity",(no_item_text % (item_off_name, possessed_quantity))))
                # Error, can't afford sell
                return
            #print(item_off_name,pd_price,shard_price) good for debugging
            if pd_price != '--': # If the item sells for pd
                # Load user's pd balance
                pd_balance = read_sheets(SERVER_INVENTORY_DB,tab_name+PD_BAL_LOC)[0]
                pd_balance = pd_balance[0]
                pd_payment = int(int(pd_price)*int(quantity)/4) # Calculate payment in pd
                pd_balance = int(pd_balance)+pd_payment # calculate new balance
                # Write new balance to google sheet
                write_sheets(SERVER_INVENTORY_DB,tab_name+PD_BAL_LOC,pd_balance,0)
                sell_embed=discord.Embed(title="",description=(sell_success_text_pd % (quantity,item_off_name,pd_payment)), color=fall_auburn)
            elif shard_price != '--': # If the item sells for shards
                # Load user's shard balance
                shard_balance = read_sheets(SERVER_INVENTORY_DB,tab_name+SHARD_BAL_LOC)[0]
                shard_balance = shard_balance[0]
                shard_payment = int(int(shard_price)*int(quantity)/4) # Calculate payment in shards
                shard_balance = int(shard_balance) + shard_payment # calculate new balance
                # Write new balance to google sheet
                write_sheets(SERVER_INVENTORY_DB,tab_name+SHARD_BAL_LOC,shard_balance,0)
                sell_embed=discord.Embed(title="",description=(sell_success_text_shards % (quantity,item_off_name,shard_payment)), color=fall_auburn)
            # Write updated inventory to google sheet (clear it first to force update)
            clear_sheets(SERVER_INVENTORY_DB,tab_name+INVENTORY_LOC)
            write_sheets(SERVER_INVENTORY_DB,tab_name+INVENTORY_LOC,user_inventory)
            sell_embed.set_author(name="Successfully Sold", icon_url=sell_icon)
            await ctx.send(embed=sell_embed)
            # Display information to user
        else:
            await ctx.send(embed=send_error_msg("Error: Member Database Error",(no_inventory_tab % user.split('#')[0])))
    else:
        await ctx.send(embed=send_maintenance_msg())

# GIFT COMMANDS PAGE 3 COMMANDS 3 and 4, PAGE 4 COMMANDS 1 and 2
@commands.has_any_role("Tenants","Interns","Mods","Dev")
@bot.command(name='gift',ignore_extra=False) #Bot gifts the target user a specified quantity of specified item
async def critter_gift(ctx,command_ext="NULL",ex_arg_1="NULL",ex_arg_2="NULL",ex_arg_3="NULL"):
    global maintenance #maintenance check
    error = False
    if maintenance:
        if command_ext != "special":
            if ex_arg_3 != "NULL": #Check if we took on too many args
                await ctx.send(embed=send_error_msg("Error: Bamboozled",too_many_args))
                return
            if command_ext == "NULL" or ex_arg_1 == "NULL" or ex_arg_2 == "NULL":
                #Check if we took too few args
                arg_txt=find_args(ctx.message.content)
                await ctx.send(embed=send_error_msg("Error: Missing Argument",(missed_argument % arg_txt)))
                return
            # Align args with c!gift
            target_user = command_ext
            item = ex_arg_1
            quantity = ex_arg_2
            print(target_user)
            # Load in config items (banned items, and gift fee)
            banned_items = read_sheets(CRITTER_CONFIG_ID,BANNED_GIFT_LOC)
            gift_fee = read_sheets(CRITTER_CONFIG_ID,GIFT_FEE_LOC)[0]
            gift_fee = gift_fee[0]
            if quantity.isdigit(): # Need Number for quantity
                if int(quantity) <= 0: # Number has to be positive
                    await ctx.send(embed=send_error_msg("Error: Invalid Number of Items",inv_quantity_text))
                    #Error bad quantity
                    error = True
            else:
                await ctx.send(embed=send_error_msg("Error: Invalid Number of Items",inv_quantity_text))
                #Error bad quantity
                error = True
            # Check if valid item/quantity to pull from inventory and have the money for fee
            if item.lower() in [banned_item[0].lower() for banned_item in banned_items]:
                await ctx.send(embed=send_error_msg("Error: This is an Ungiftable Item",banned_item_text % item))
                error = True
            item_off_name = "" # Initialize the Official Item Name
            # Load in all items from the shop
            all_items = read_sheets_multiple(CRITTER_CONFIG_ID,ALL_ITEMS_LOC)
            for shop_item in all_items: # Go through the items one by one
                if shop_item[0].lower() == item.lower().replace("’","'"): # Check for a match with argument
                    item_off_name = shop_item[0] #Grab official name
                    pd_price = shop_item[1].strip() #Grab price in pd
                    shard_price = shop_item[2].strip() #Grab price in shards
            if item.lower() == "pd": #PD is a giftable item, but not in the shop
                item_off_name = "PD"
                pd_price = '1' # Each PD costs one PD, imagine that
                shard_price = '--'
            if not item_off_name: # If we didn't match there's no official name
                # Error, invalid item
                await ctx.send(embed=send_error_msg("Error: This is an Ungiftable Item",(banned_item_text % item)))
                error = True
            elif not shard_price == "--": # If it's a shard item, it's a no go for gifting
                # Error, banned item
                await ctx.send(embed=send_error_msg("Error: This is an Ungiftable Item",banned_item_text % item))
                error = True
            #print(item_off_name,pd_price,shard_price) good for debugging
            # Update the user inventory mapping by pulling sheets user data
            users_info = read_sheets(CRITTER_CONFIG_ID,USER_INFO_LOC)
            # Convert 2d Lists into 1d Lists (just pulled column data)
            user_full_names = [user[0] for user in users_info]
            user_inv_names = [user[1] for user in users_info]
            # Combines this into dictionary
            user_inventory_map = dict(zip(user_full_names,user_inv_names))
            user = str(ctx.message.author) # Grab user info for inventory compare
            try: # Try to grab user name from argument
                arg_user_name = str(await bot.fetch_user(target_user[2:-1].replace("!",'')))
            except:
                await ctx.send(embed=send_error_msg("Error: Unknown User",unknown_user))
                return
            print(arg_user_name)
            if arg_user_name == user:
                await ctx.send(embed=send_error_msg("Error: One is the Loneliest Number",gift_self))
                return
            if error:
                return
            if user in user_inventory_map: #verify user is in the inventory map
                gifter_tab_name =  user_inventory_map[user] #grab inventory tab name
                user_inventory = read_sheets(SERVER_INVENTORY_DB,gifter_tab_name+INVENTORY_LOC)
                # read in the user inventory
                pd_balance = read_sheets(SERVER_INVENTORY_DB,gifter_tab_name+PD_BAL_LOC)[0]
                pd_balance = pd_balance[0]
                # Load user's pd balance
                found = False # Marker if we found the item in the user's inventory
                possessed_quantity = 0
                for entry in user_inventory: # Check if item in inventory
                    if entry[0].lower() == item.lower():
                        possessed_quantity = int(entry[1])
                        if possessed_quantity >= int(quantity):
                            # If the item is in the inventory, update quantity
                            entry[1] = str(int(entry[1]) - int(quantity))
                            found = True
                            if entry[1] == '0': # If the user no longer has any of the item
                                user_inventory.remove(entry) #remove it
                            break
                if item_off_name == "PD": #If we're gifting PD pull it from the inventory
                    # Don't have to check for enough, do that with taxes
                    pd_balance = int(pd_balance)-int(quantity)
                    found = True
                if not found: # If item not in inventory, error
                    await ctx.send(embed=send_error_msg("Error: Lacking Item Quantity",(no_item_text % (item_off_name, possessed_quantity))))
                    # Error, can't afford gift
                    return
                gift_tax = max(int((int(gift_fee)*int(quantity)*int(pd_price)/100)),1)
                if int(pd_balance) < gift_tax: # If you can't afford the tax
                    # If couldn't afford PD gift we'll end up here anyway
                    await ctx.send(embed=send_error_msg("Error: Unable to Cover Gift Fee",gift_tax_expense_text % (gift_tax,gift_tax-int(pd_balance))))
                    # Error, can't afford gift
                    return
                #load in critter's balance
                critter_balance_var = read_sheets(SERVER_INVENTORY_DB,CRITTER_BALANCE_LOC)[0]
                critter_balance_var = int(critter_balance_var[0])
                critter_balance_var += gift_tax # calculate critter's profits
                pd_balance = int(pd_balance)-gift_tax # calculate new balance
                # Set up all variables for write, but only write if user confirms gift
            else:
                await ctx.send(embed=send_error_msg("Error: Member Database Error",(no_inventory_tab % user.split('#')[0])))
                return
            if arg_user_name in user_inventory_map: #If the target user exists in the mapping
                # Load the giftee's inventory tab, inventory and pd_balance
                giftee_tab_name = user_inventory_map[arg_user_name]
                giftee_balance = read_sheets(SERVER_INVENTORY_DB,giftee_tab_name+PD_BAL_LOC)[0]
                giftee_balance = giftee_balance[0]
                giftee_inventory = read_sheets(SERVER_INVENTORY_DB,giftee_tab_name+INVENTORY_LOC)
                if item_off_name == "PD": # If the giftee receives PD, add to balance
                    giftee_balance = int(giftee_balance)+int(quantity)
                    PD_given = int(quantity)
                else: # If they receive an item, gotta go the long way
                    found = False
                    PD_given = 0
                    for entry in giftee_inventory: # Look for item in inventory
                        if entry[0] == item_off_name:
                            # If the item is in the inventory, update quantity
                            entry[1] = str(int(entry[1]) + int(quantity))
                            found = True
                            break
                    if not found: # If its not in the inventory, add it
                        new_entry = [item_off_name,quantity]
                        giftee_inventory.append(new_entry)
                # Set up all variables for write, but only write if user confirms gift
            else: #Invalid user (not in the mapping)
                await ctx.send(embed=send_error_msg("Error: Member Database Error",(no_inventory_tab % arg_user_name.split('#')[0])))
                return
            dm_user = await bot.fetch_user(target_user[2:-1].replace("!",''))
            # Output proposed action to user
            gift_question = (gift_question_text % (int(quantity),item_off_name,str(dm_user.name),gift_tax+PD_given))
            embed=discord.Embed(title="",description=gift_question, color=fall_auburn)
            embed.set_author(name="Are You Sure?", icon_url=gift_orng_icon)
            gift = await ctx.send(embed=embed)
            # Give the user option to confirm or reject
            for emoji in emoji_confirm:
                await gift.add_reaction(emoji)
            while 1: # Needs to accept reactions until timeout or we see a valid reaction
                try:
                    # Wait for user to react and store that info
                    reaction, user = await bot.wait_for('reaction_add',timeout=15)
                    react_author = user.name+"#"+user.discriminator
                    if (react_author == str(ctx.message.author)) and (reaction.emoji in emoji_confirm): #only the user who initiated can accept/cancel gift
                        if reaction.emoji == emoji_confirm[0]: # User confirms gift
                            try:
                                await dm_user.create_dm()
                            except:
                                embed=discord.Embed(title="",description=(gift_dm_error % arg_user_name.split("#")[0]), color=reject_red)
                                embed.set_author(name="Gift Undeliverable", icon_url=error_icon)
                                await gift.edit(embed=embed) #Actually updates the embed
                                await gift.clear_reactions() #Clears reactions
                                return # Exit after timeout
                            # Do all the writes
                            # Write new gifter balance to google sheet
                            write_sheets(SERVER_INVENTORY_DB,gifter_tab_name+PD_BAL_LOC,pd_balance,0)
                            # Write updated gifter inventory to google sheet (clear it first to force update)
                            clear_sheets(SERVER_INVENTORY_DB,gifter_tab_name+INVENTORY_LOC)
                            write_sheets(SERVER_INVENTORY_DB,gifter_tab_name+INVENTORY_LOC,user_inventory)
                            # Write updated giftee inventory/balance to google sheet
                            write_sheets(SERVER_INVENTORY_DB,giftee_tab_name+PD_BAL_LOC,giftee_balance,0)
                            write_sheets(SERVER_INVENTORY_DB,giftee_tab_name+INVENTORY_LOC,giftee_inventory)
                            # Write updated balance to critter
                            write_sheets(SERVER_INVENTORY_DB,CRITTER_BALANCE_LOC,critter_balance_var,0)
                            #Tells user what they gave and to whom
                            gift_receipt = (gift_receipt_text % (str(dm_user.name),str(ctx.message.author.name),str(dm_user.name),item_off_name,int(quantity),gift_tax,gift_tax+PD_given))
                            embed=discord.Embed(title="",description=gift_receipt, color=success_green)
                            embed.set_author(name="Gifting Successful", icon_url=gift_grn_icon)
                            #Tells the recipient what they were given and from whom
                            gift_msg_txt = (gift_message_text % (str(ctx.message.author.name),int(quantity),item_off_name))
                            gift_msg_embed=discord.Embed(title="",description=gift_msg_txt,color=success_green)
                            gift_msg_embed.set_author(name="Gift Received!",icon_url=gift_grn_icon)
                            await dm_user.dm_channel.send(embed=gift_msg_embed)
                        else: # User cancels gift
                            embed=discord.Embed(title="",description=gift_cancel, color=reject_red)
                            embed.set_author(name="Gifting Canceled", icon_url=gift_red_icon)
                            # No writes performed, all the calculated changes just go away
                            # Kind of a waste, but I like the structure of the program better this way
                            # it has to do most of that math to check if it can be done anyhow
                        await gift.edit(embed=embed) #Actually updates the embed
                        await gift.clear_reactions() #Clears reactions
                        return # We only do this once
                except: #should pretty much only happen in timeout
                    # Let user know that request timed out
                    embed=discord.Embed(title="",description=gift_timeout, color=reject_red)
                    embed.set_author(name="Gifting Timeout", icon_url=error_icon)
                    await gift.edit(embed=embed) #Actually updates the embed
                    await gift.clear_reactions() #Clears reactions
                    return # Exit after timeout
        else:
            # Update the user inventory mapping by pulling sheets user data
            users_info = read_sheets(CRITTER_CONFIG_ID,USER_INFO_LOC)
            # Convert 2d Lists into 1d Lists (just pulled column data)
            user_full_names = [user[0] for user in users_info]
            user_inv_names = [user[1] for user in users_info]
            # Combines this into dictionary
            user_inventory_map = dict(zip(user_full_names,user_inv_names))
            user = str(ctx.message.author) # Grab user info for inventory compare
            if user in user_inventory_map: #verify user is in the inventory map
                gifter_tab_name =  user_inventory_map[user] #grab inventory tab name
                user_inventory = read_sheets(SERVER_INVENTORY_DB,gifter_tab_name+INVENTORY_LOC)
                user_item_list = [item[0].lower() for item in user_inventory]
                jumbo_items_load = read_sheets(CRITTER_CONFIG_ID,GIFT_ITEM_GUIDE_JUMBO)
                reg_items_load = read_sheets(CRITTER_CONFIG_ID,GIFT_ITEM_GUIDE_REG)
                shard_balance = read_sheets(SERVER_INVENTORY_DB,gifter_tab_name+SHARD_BAL_LOC)[0]
                shard_balance = int(shard_balance[0])
                jumbo_items=[]
                jumbo_items_lower=[]
                jumbo_items_full=[]
                shard_max_jumbo=0
                for usable,item_name in jumbo_items_load:
                    if "Shards" in item_name:
                        if shard_balance > 0:
                            shard_min = 1
                            shard_max_jumbo = min(shard_balance,int(item_name.split('-')[1].split(' ')[0]))
                            #print(shard_min,shard_max)
                            jumbo_items.append("%i-%i Shards" % (shard_min,shard_max_jumbo))
                    if usable == "Yes":
                        jumbo_items_full.append(item_name)
                        if item_name.lower().replace("’","'") in user_item_list:
                            if item_name.lower() == "jumbo gift bag":
                                if int(user_inventory[user_item_list.index(item_name.lower())][1]) > 1:
                                    jumbo_items.append(item_name)
                                    jumbo_items_lower.append(item_name.lower())
                            else:
                                jumbo_items.append(item_name)
                                jumbo_items_lower.append(item_name.lower())
                reg_items=[]
                reg_items_lower=[]
                reg_items_full=[]
                shard_max_reg=0
                for usable,item_name in reg_items_load:
                    if "Shards" in item_name:
                        if shard_balance > 0:
                            shard_min = 1
                            shard_max_reg = min(shard_balance,int(item_name.split('-')[1].split(' ')[0]))
                            #print(shard_min,shard_max)
                            reg_items.append("%i-%i Shards" % (shard_min,shard_max_reg))
                    if usable == "Yes":
                        reg_items_full.append(item_name)
                        if item_name.lower().replace("’","'") in user_item_list:
                            if item_name.lower() == "gift bag":
                                if int(user_inventory[user_item_list.index(item_name.lower())][1]) > 1:
                                    reg_items.append(item_name)
                                    reg_items_lower.append(item_name.lower())
                            else:
                                reg_items.append(item_name)
                                reg_items_lower.append(item_name.lower())
            else:
                await ctx.send(embed=send_error_msg("Error: Member Database Error",(no_inventory_tab % user.split('#')[0])))
                return
            if ex_arg_1.lower() == "menu":
                bag_type_arg = ex_arg_2
                if ex_arg_3 != "NULL":
                    await ctx.send(embed=send_error_msg("Error: Bamboozled",too_many_args))
                    return
                if bag_type_arg == "NULL":
                    jumbo_items = [jumbo_item for jumbo_item in jumbo_items if not (jumbo_item in reg_items)]
                    embed=discord.Embed(title="",description=gift_via_help_descr, color=help_orange)
                    embed.set_author(name="Gifting Inventory", icon_url=gift_orng_icon)
                    embed.add_field(name="Gift Bag:",value=("```%s```" % tablify_list(reg_items)),inline=False)
                    embed.add_field(name="Jumbo Gift Bag:",value=("```%s```" % tablify_list(jumbo_items)),inline=False)
                    await ctx.send(embed=embed)
                elif bag_type_arg.lower().strip() == "gift bag":
                    embed=discord.Embed(title="",description=("```%s```" % tablify_list(reg_items_full)), color=help_orange)
                    embed.set_author(name="Gift Bag Items:", icon_url=gift_orng_icon)
                    await ctx.send(embed=embed)
                elif bag_type_arg.lower().strip() == "jumbo gift bag":
                    embed=discord.Embed(title="",description=("```%s```" % tablify_list(jumbo_items_full)), color=help_orange)
                    embed.set_author(name="Jumbo Gift Bag Items:", icon_url=gift_orng_icon)
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(embed=send_error_msg("Error: Invalid Command",gift_via_help_options))
            else:
                # Align args with c!gift special
                recipient_id = ex_arg_1
                item_arg = ex_arg_2.replace("’","'")
                bag_type_arg = ex_arg_3
                if recipient_id == "NULL" or item_arg == "NULL" or bag_type_arg == "NULL": #Checks for missing arguments
                    arg_txt="recipient name, item name or gift bag type"
                    await ctx.send(embed=send_error_msg("Error: Missing Argument",(missed_argument % arg_txt)))
                    return
                #print(user_inventory) #good for debugging
                try: # Try to grab user name from argument
                    arg_user_name = str(await bot.fetch_user(recipient_id[2:-1].replace("!",'')))
                except: #Unknown user
                    await ctx.send(embed=send_error_msg("Error: Unknown User",unknown_user))
                    return
                if arg_user_name == user: #Gifting to yourself
                    await ctx.send(embed=send_error_msg("Error: One is the Loneliest Number",gift_self))
                    return
                gifted_item_name = ""
                bag_type = ""
                if bag_type_arg.lower().strip() == "gift bag": #Sending a gift bag
                    bag_type = "Gift Bag"
                    if bag_type_arg.lower().strip() not in user_item_list: #Don't have a gift bag
                        await ctx.send(embed=send_error_msg("Error: Missing Bag Type",(no_gift_bags % bag_type)))
                        return
                    else: #Deduct 1 gift bag from inventory
                        user_inventory[user_item_list.index(bag_type_arg.lower().strip())][1] = str(int(user_inventory[user_item_list.index(bag_type_arg.lower().strip())][1]) - 1)
                    if not item_arg.lower().strip() in reg_items_lower: #Item is not in the list of gift bag items user can send
                        if len(item_arg.lower().strip().split(" ")) != 2:
                            await ctx.send(embed=send_error_msg("Error: Problematic Item",(un_bag_item % item_arg.lower().strip())))
                            return
                        if "shards" == item_arg.lower().strip().split(" ")[1]:
                        #User is sending shards, ensure its properly formatted and deduct shards from inventory
                            num_shards = item_arg.lower().strip().split(" ")[0]
                            if not num_shards.isdigit():
                                await ctx.send(embed=send_error_msg("Error: Unexpected Formatting",gift_shards_format))
                                return
                            if int(num_shards) == 0:
                                await ctx.send(embed=send_error_msg("Error: Why Would You Do That",gift_no_shards_dunk))
                                return
                            if int(num_shards) <= shard_balance:
                                if int(num_shards) > shard_max_reg:
                                    await ctx.send(embed=send_error_msg("Error: Not Enough Space in This Gift Bag",gift_bag_shard_lim_text))
                                    return
                                shard_balance -= int(num_shards)
                                gifted_item_name = str(num_shards)+" Shard(s)"
                            else:
                                await ctx.send(embed=send_error_msg("Error: Not Enough Shards",(gift_low_shards % (int(num_shards),shard_balance))))
                                return
                        else:
                            await ctx.send(embed=send_error_msg("Error: Problematic Item",(un_bag_item % item_arg.lower().strip())))
                            return
                    if item_arg.lower().strip() == "gift bag": #The user is gifting a gift bag
                        if int(user_inventory[user_item_list.index(item_arg.lower().strip())][1]) < 1:
                            #Ensures there's still a gift bag in the inventory to send in a gift bag
                            await ctx.send(embed=send_error_msg("Error: Insufficient Bag Quantity",(not_enough_bags %(item_arg,bag_type,bag_type))))
                            return
                    if not gifted_item_name: # If we haven't taken shards from the inventory
                        #Take the item from the inventory and grab its official name
                        user_inventory[user_item_list.index(item_arg.lower().strip())][1] = str(int(user_inventory[user_item_list.index(item_arg.lower().strip())][1]) - 1)
                        gifted_item_name = user_inventory[user_item_list.index(item_arg.lower().strip())][0]
                elif bag_type_arg.lower().strip() == "jumbo gift bag": #Sending a jumbo gift bag
                    bag_type = "Jumbo Gift Bag"
                    if bag_type_arg.lower().strip() not in user_item_list: #Don't have a jumbo gift bag
                        await ctx.send(embed=send_error_msg("Error: Missing Bag Type",(no_gift_bags % bag_type)))
                        return
                    else: #Deduct 1 jumbo gift bag from inventory
                        user_inventory[user_item_list.index(bag_type_arg.lower().strip())][1] = str(int(user_inventory[user_item_list.index(bag_type_arg.lower().strip())][1]) - 1)
                    if not item_arg.lower().strip() in jumbo_items_lower:
                        if len(item_arg.lower().strip().split(" "))!=2:
                            await ctx.send(embed=send_error_msg("Error: Problematic Item",(un_bag_item % item_arg.lower().strip())))
                            return
                        if "shards" == item_arg.lower().strip().split(" ")[1]:
                        #User is sending shards, ensure its properly formatted and deduct shards from inventory
                            num_shards = item_arg.lower().strip().split(" ")[0]
                            if not num_shards.isdigit():
                                await ctx.send(embed=send_error_msg("Error: Unexpected Formatting",gift_shards_format))
                                return
                            if int(num_shards) == 0:
                                await ctx.send(embed=send_error_msg("Error: Why Would You Do That",gift_no_shards_dunk))
                                return
                            #print(num_shards,shard_max_jumbo) #good for debugging
                            if int(num_shards) <= shard_balance:
                                if int(num_shards) > shard_max_jumbo:
                                    await ctx.send(embed=send_error_msg("Error: Not Enough Space in This Gift Bag",gift_bag_shard_lim_text))
                                    return
                                #print(shard_balance) #good for debugging
                                shard_balance -= int(num_shards)
                                gifted_item_name = str(num_shards)+" Shard(s)"
                                #print(shard_balance) #good for debugging
                            else:
                                await ctx.send(embed=send_error_msg("Error: Not Enough Shards",(gift_low_shards % (int(num_shards),shard_balance))))
                                return
                        else:
                            await ctx.send(embed=send_error_msg("Error: Problematic Item",(un_bag_item % item_arg.lower().strip())))
                            return
                    if item_arg.lower().strip() == "jumbo gift bag": #The user is gifting a jumbo gift bag
                        if int(user_inventory[user_item_list.index(item_arg.lower().strip())][1]) < 1:
                            #Ensures there's still a gift bag in the inventory to send in a jumbo gift bag
                            await ctx.send(embed=send_error_msg("Error: Insufficient Bag Quantity",(not_enough_bags %(item_arg,bag_type,bag_type))))
                            return
                    if not gifted_item_name: # If we haven't taken shards from the inventory
                        #Take the item from the inventory and grab its official name
                        user_inventory[user_item_list.index(item_arg.lower().strip())][1] = str(int(user_inventory[user_item_list.index(item_arg.lower().strip())][1]) - 1)
                        gifted_item_name = user_inventory[user_item_list.index(item_arg.lower().strip())][0]
                else: #Invalid Bag Type
                    await ctx.send(embed=send_error_msg("Error: This Item Needs a Gift Bag",gift_special_invalid_bag))
                    return
                # Clean out any "zeroed" items from the gifter's inventory (can be more than 1 including bags)
                upd_usr_inv = [entry for entry in user_inventory if entry[1]!='0']
                #print(upd_usr_inv) #good for debugging
                if arg_user_name in user_inventory_map: # Grab giftee's inventory
                    giftee_tab_name = user_inventory_map[arg_user_name]
                    if "Shard(s)" in gifted_item_name: #If we're giving out shards, load and adjust shard balance
                        giftee_shard_bal = read_sheets(SERVER_INVENTORY_DB,giftee_tab_name+SHARD_BAL_LOC)[0]
                        giftee_shard_bal = str(int(giftee_shard_bal[0])+int(num_shards))
                    else: #Otherwise add the item to their inventory
                        giftee_found = False
                        giftee_inventory = read_sheets(SERVER_INVENTORY_DB,giftee_tab_name+INVENTORY_LOC)
                        for ind in range(len(giftee_inventory)):
                            if gifted_item_name == giftee_inventory[ind][0]:
                                giftee_inventory[ind][1] = str(int(giftee_inventory[ind][1]) + 1)
                                giftee_found = True
                        if not giftee_found:
                            giftee_inventory.append([gifted_item_name,'1'])
                else:
                    await ctx.send(embed=send_error_msg("Error: Member Database Error",(no_inventory_tab % arg_user_name.split('#')[0])))
                    return
                # Output proposed action to user
                gift_question = (gift_bag_question_text % (gifted_item_name,arg_user_name.split("#")[0],bag_type))
                embed=discord.Embed(title="",description=gift_question, color=fall_auburn)
                embed.set_author(name="Are You Sure?", icon_url=gift_orng_icon)
                gift = await ctx.send(embed=embed)
                dm_user = await bot.fetch_user(recipient_id[2:-1].replace("!",''))
                # Give the user option to confirm or reject
                for emoji in emoji_confirm:
                    await gift.add_reaction(emoji)
                while 1: # Needs to accept reactions until timeout or we see a valid reaction
                    try:
                        # Wait for user to react and store that info
                        reaction, user = await bot.wait_for('reaction_add',timeout=15)
                        react_author = user.name+"#"+user.discriminator
                        if (react_author == str(ctx.message.author)) and (reaction.emoji in emoji_confirm): #only the user who initiated can accept/cancel gift
                            if reaction.emoji == emoji_confirm[0]: # User confirms gift
                                try:
                                    await dm_user.create_dm()
                                except:
                                    embed=discord.Embed(title="",description=(gift_dm_error % arg_user_name.split("#")[0]), color=reject_red)
                                    embed.set_author(name="Gift Undeliverable", icon_url=error_icon)
                                    await gift.edit(embed=embed) #Actually updates the embed
                                    await gift.clear_reactions() #Clears reactions
                                    return # Exit after timeout
                                # Do all the writes
                                # Write new gifter balance to google sheet
                                write_sheets(SERVER_INVENTORY_DB,gifter_tab_name+SHARD_BAL_LOC,shard_balance,0)
                                # Write updated gifter inventory to google sheet (clear it first to force update)
                                clear_sheets(SERVER_INVENTORY_DB,gifter_tab_name+INVENTORY_LOC)
                                write_sheets(SERVER_INVENTORY_DB,gifter_tab_name+INVENTORY_LOC,upd_usr_inv)
                                # Write updated giftee inventory/balance to google sheet
                                if "Shard(s)" in gifted_item_name:
                                    write_sheets(SERVER_INVENTORY_DB,giftee_tab_name+SHARD_BAL_LOC,giftee_shard_bal,0)
                                else:
                                    write_sheets(SERVER_INVENTORY_DB,giftee_tab_name+INVENTORY_LOC,giftee_inventory)
                                #Critter makes no money :(
                                #Tells user what they gave and to whom
                                gift_receipt = (gift_bag_receipt_text % (str(dm_user.name),str(ctx.message.author.name),str(dm_user.name),gifted_item_name,bag_type))
                                embed=discord.Embed(title="",description=gift_receipt, color=success_green)
                                embed.set_author(name="Gifting Successful", icon_url=gift_grn_icon)
                                #Tells the recipient what they were given and from whom
                                if "Shard(s)" in gifted_item_name:
                                    gift_msg_txt = (gift_message_shard_text % (str(ctx.message.author.name),gifted_item_name))
                                else:
                                    gift_msg_txt = (gift_message_text % (str(ctx.message.author.name),1,gifted_item_name))
                                gift_msg_embed=discord.Embed(title="",description=gift_msg_txt,color=success_green)
                                gift_msg_embed.set_author(name="Gift Received!",icon_url=gift_grn_icon)
                                print("RIGHT HERE")
                                await dm_user.dm_channel.send(embed=gift_msg_embed)
                            else: # User cancels gift
                                embed=discord.Embed(title="",description=gift_cancel, color=reject_red)
                                embed.set_author(name="Gifting Canceled", icon_url=gift_red_icon)
                                # No writes performed, all the calculated changes just go away
                                # Kind of a waste, but I like the structure of the program better this way
                                # it has to do most of that math to check if it can be done anyhow
                            await gift.edit(embed=embed) #Actually updates the embed
                            await gift.clear_reactions() #Clears reactions
                            return # We only do this once
                    except: #should pretty much only happen in timeout
                        # Let user know that request timed out
                        embed=discord.Embed(title="",description=gift_bag_timeout, color=reject_red)
                        embed.set_author(name="Gifting Timeout", icon_url=error_icon)
                        await gift.edit(embed=embed) #Actually updates the embed
                        await gift.clear_reactions() #Clears reactions
                        return # Exit after timeout
    else:
        await ctx.send(embed=send_maintenance_msg())

# EXCHANGE SHARDS COMMAND COMMAND PAGE 4 COMMAND 3
@commands.has_any_role("Tenants","Interns","Mods","Dev")
@bot.command(name='exchange',ignore_extra=False) #Bot exchanges the specified quantity of shards for PD
async def critter_exchange(ctx,command_ext="NULL",quantity="NULL"):
    global maintenance #maintenance check
    if maintenance:
        if command_ext.lower() == 'shards': #Only case is exchange shards
            if quantity == "NULL":
                arg_txt=find_args(ctx.message.content)
                await ctx.send(embed=send_error_msg("Error: Missing Argument",(missed_argument % arg_txt)))
                return
            exchange_rate = read_sheets(CRITTER_CONFIG_ID,EXCHANGE_RATE_LOC)[0]
            exchange_rate = exchange_rate[0]
            user_name = str(ctx.message.author)
            if quantity.isdigit(): # Need Number for quantity
                if int(quantity) <= 0: # Number has to be positive
                    await ctx.send(embed=send_error_msg("Error: Invalid Number of Shards",inv_quantity_text))
                    #Error invalid quantity
                    return
            else:
                await ctx.send(embed=send_error_msg("Error: Invalid Number of Shards",inv_quantity_text))
                #Error invalid quantity
                return
            # Update the user inventory mapping by pulling sheets user data
            users_info = read_sheets(CRITTER_CONFIG_ID,USER_INFO_LOC)
            # Convert 2d Lists into 1d Lists (just pulled column data)
            user_full_names = [user[0] for user in users_info]
            user_inv_names = [user[1] for user in users_info]
            # Combines this into dictionary
            user_inventory_map = dict(zip(user_full_names,user_inv_names))
            user = str(ctx.message.author) #Grab user info from author
            if user in user_inventory_map: #verify user is in the inventory map
                tab_name =  user_inventory_map[user] #grab inventory tab name
                # Load PD and shard balances from user inventory tab
                pd_balance = read_sheets(SERVER_INVENTORY_DB,tab_name+PD_BAL_LOC)[0]
                pd_balance = pd_balance[0]
                shard_balance = read_sheets(SERVER_INVENTORY_DB,tab_name+SHARD_BAL_LOC)[0]
                shard_balance = shard_balance[0]
                if int(quantity) > int(shard_balance): # If user doesn't have enough shards
                     await ctx.send(embed=send_error_msg("Error: Insufficient Shard Funds",(not_enough_shards % (int(shard_balance)))))
                     # Error, not enough shards
                     return
            else: #Invalid user (not in the mapping)
                await ctx.send(embed=send_error_msg("Error: Member Database Error",(no_inventory_tab % user.split('#')[0]))) #Error, invalid user
                return
            # Update PD and Shard balances based on exchange
            pd_balance = int(pd_balance)+int(quantity)*int(exchange_rate)
            shard_balance = int(shard_balance)-int(quantity)
            # Write updated balances to the sheet
            write_sheets(SERVER_INVENTORY_DB,tab_name+PD_BAL_LOC,pd_balance,0)
            write_sheets(SERVER_INVENTORY_DB,tab_name+SHARD_BAL_LOC,shard_balance,0)
            # Output to discord server on completion
            exchng_embed=discord.Embed(title="",description=(exchange_success_text % (quantity,int(quantity)*int(exchange_rate))), color=function_pink)
            exchng_embed.set_author(name="Shards Exchanged Successfully", icon_url=exchange_icon)
            await ctx.send(embed=exchng_embed)
        else: #No other use of "exchange" primary command
            await ctx.send(embed=send_error_msg("Error: Command Error",invalid_command))
    else:
        await ctx.send(embed=send_maintenance_msg())

# SUGGEST COMMAND PAGE 4 COMMAND 4
@commands.has_any_role("Tenants","Interns","Mods","Dev")
@bot.command(name='suggest',ignore_extra=False)#User makes a suggestion to the mods
async def critter_suggest(ctx,*,suggestion):
    global maintenance #maintenance check
    if maintenance:
        user_name = str(ctx.message.author.name)
        await ctx.message.delete() #Hide user suggestion from others
        # Send user some output so their suggestion doesn't dissappear into a vaccuum
        sugg_embed=discord.Embed(title="",description=suggestion_ack_text, color=fall_auburn)
        sugg_embed.set_author(name="Suggestion Successfully Submitted", icon_url=suggest_icon)
        await ctx.send(embed=sugg_embed)
        #Sends the mods the suggestion
        channel = bot.get_channel(MODS) #Grab the channel to send suggestion in
        dt_date = datetime.datetime.now()
        date = dt_date.strftime('%m/%d/%Y')
        sugg_embed=discord.Embed(title="",description=(suggestion_send_text % suggestion.strip('""').strip("''")), color=fall_auburn)
        sugg_embed.set_author(name=("%s Suggests:" % user_name), icon_url=suggest_icon)
        sugg_embed.set_footer(text=(suggestion_footer % date))
        await channel.send(embed=sugg_embed)#Give user suggestion to the mods
    else:
        await ctx.send(embed=send_maintenance_msg())

# ODDS COMMAND PAGE 4 COMMAND 5
@commands.has_any_role("Tenants","Interns","Mods","Dev")
@bot.command(name='odds',ignore_extra=False) #User fights a horror of specified type
async def critter_odds(ctx,horror_type,courage_level,opt_item_or_curse="",optional_curse=""):
    global maintenance #maintenance check
    error = False
    if maintenance:
        victory = False # If the user wins against the horror
        banished = False # If the user banishes the horror
        item_used = False # If the user uses item(s)
        curse_used = False # If the user uses curse(s)
        # Loads in optional item(s) and/or curse(s) as comma separated lists
        param_1_list = [elem.strip().lower().replace("’","'") for elem in opt_item_or_curse.split(",")]
        param_2_list = [elem.strip().lower().replace("’","'") for elem in optional_curse.split(",")]
        #print(param_1_list,param_2_list) # good for debugging
        if param_2_list != ['']:
            opt_item_list = param_1_list
            opt_curse_list = param_2_list
            item_used = True
            curse_used = True
        elif param_1_list[0][:5] == "curse":
            opt_item_list = []
            opt_curse_list = param_1_list
            curse_used = True
        elif param_1_list != ['']:
            opt_item_list = param_1_list
            opt_curse_list = []
            item_used = True
        else:
            opt_item_list = param_1_list
            opt_curse_list = param_2_list
        #print(item_used,curse_used) # good for debugging
        # Sorts argument lists to check compatibility
        opt_item_list.sort()
        opt_curse_list.sort()
        # Load in possible items and curses
        item_list = read_sheets(CRITTER_CONFIG_ID,HORROR_OPT_ITEM_LOC)
        curse_list = read_sheets(CRITTER_CONFIG_ID,HORROR_OPT_CURSE_LOC)
        # Grab "lowercase versions" to ensure maximum compatibility with args
        items = [entry[0].lower() for entry in item_list]
        curses = [entry[0].lower() for entry in curse_list]
        for ind in range(len(opt_item_list)):
            # Check argument viability (valid and compatible items)
            if not (opt_item_list[ind].lower() in items or opt_item_list[ind] == ''):
                await ctx.send(embed=send_error_msg("Error: Invalid Item",invalid_horr_item % opt_item_list[ind]))
                error = True
            else:
                if ind < len(opt_item_list)-1: # Items of the same set are incompatible
                    if opt_item_list[ind][:4] == opt_item_list[ind+1][:4]:
                        await ctx.send(embed=send_error_msg("Error: Invalid Argument",incompat_horr_item))
                        error = True
        for ind in range(len(opt_curse_list)):
            # Check argument viability (valid and compatible curses)
            if not (opt_curse_list[ind]== "" or opt_curse_list[ind].lower() in curses):
                await ctx.send(embed=send_error_msg("Error: Invalid Curse",invalid_curse % opt_curse_list[ind]))
                error = True
            else:
                if ind < len(opt_curse_list)-1: # Curses of the same type are incompatible
                    if opt_curse_list[ind][:12] == opt_curse_list[ind+1][:12]:
                        await ctx.send(embed=send_error_msg("Error: Incompatible Curses",incompat_horr_curse))
                        error = True
        #print("Lists examined; all compatible!") # good for debugging
        # Load in role info (hit chance, courage dice and horror hp)
        hit_chance = read_sheets(CRITTER_CONFIG_ID,HORROR_CHANCE_LOC)[0]
        hit_chance = int(hit_chance[0])
        courage_table = read_sheets(CRITTER_CONFIG_ID,HORROR_COURAGE_LOC)
        courages = [entry[0].lower() for entry in courage_table] # Courage levels used to match arg
        horror_hp_table = read_sheets(CRITTER_CONFIG_ID,HORROR_HP_LOC)
        horrors = [entry[0].lower() for entry in horror_hp_table] # Horror types used to match arg
        if not horror_type.lower() in horrors: # Check horror type arg viability
            await ctx.send(embed=send_error_msg("Error: Invalid Argument",invalid_horror_type))
            error = True
        if not courage_level.lower() in courages: # Check courage level arg viability
            await ctx.send(embed=send_error_msg("Error: Invalid Argument",invalid_courage_level))
            error = True
        if error:
            return
        #print("Horror type and courage level proved valid!") # good for debugging
        # Load in the reward/curse sheet data for rolling at the end
        item_rewards = read_sheets(CRITTER_CONFIG_ID,HORROR_ITEM_WIN_LOC)
        shard_rewards = read_sheets(CRITTER_CONFIG_ID,HORROR_SHARD_LOC)
        curse_penalty = read_sheets(CRITTER_CONFIG_ID,HORROR_CURSE_LOC)
        # Determine the dice and HP values based on args
        base_dice = int([int(entry[1]) for entry in courage_table if entry[0]==courage_level.lower()][0])
        base_hp = int([int(entry[1]) for entry in horror_hp_table if entry[0].lower()==horror_type.lower()][0])
        if "banishing sigil" in opt_item_list: #If you banished the horror bypass some stuff
            banished = True
        # Initialize modifiers for item/curse modification
        hit_chance_mod = 0
        courage_mod = 0
        horror_hp_mod = 0
        shard_mul = 1
        #print("Determined HP and initialized modifiers!") # good for debugging
        first_param_list = []
        sec_param_list = []
        if item_used and curse_used:
            #Item and curse specified
            #print("Item and curse!") #good for debugging
            for chosen_curse in opt_curse_list: # For each curse passed
                #Find the effect of the curse
                curse_effect = ([entry[1] for entry in curse_list if entry[0].lower()==chosen_curse.lower()][0])
                curse_name = ([entry[0] for entry in curse_list if entry[0].lower()==chosen_curse.lower()][0])
                first_param_list.append(curse_name)
                if curse_effect == "Decrease Courage": # Curse decreases dice numbers
                    curse_effect_table = read_sheets(CRITTER_CONFIG_ID,HORROR_COURAGE_DEC_LOC)
                    courage_mod -= int([int(entry[1]) for entry in curse_effect_table if entry[0].lower()==chosen_curse.lower()][0])
                    #print(courage_mod,chosen_curse,curse_effect) good for debugging
                elif curse_effect == "Hit Chance Modifier": #Curse makes it harder to hit horror
                    curse_effect_table = read_sheets(CRITTER_CONFIG_ID,HORROR_CHANCE_MOD_LOC)
                    hit_chance_mod += int([int(entry[1]) for entry in curse_effect_table if entry[0].lower()==chosen_curse.lower()][0])-hit_chance
                    #print(hit_chance,hit_chance_mod,chosen_curse,curse_effect) good for debugging
                elif curse_effect == "Horror HP Increase": #Curse increases horror HP
                    curse_effect_table = read_sheets(CRITTER_CONFIG_ID,HORROR_HP_INC_LOC)
                    horror_hp_mod += int([int(entry[1]) for entry in curse_effect_table if entry[0].lower()==chosen_curse.lower()][0])
                    #print(horror_hp_mod,chosen_curse,curse_effect) good for debugging
            for chosen_item in opt_item_list: #For each item passed
                item_effect = ([entry[1] for entry in item_list if entry[0].lower()==chosen_item.lower()][0])
                #Find the effect of the item
                item_name_full = ([entry[0] for entry in item_list if entry[0].lower()==chosen_item.lower()][0])
                sec_param_list.append(item_name_full)
                if item_effect == "Increase Courage":# Item increases dice numbers
                    item_effect_table = read_sheets(CRITTER_CONFIG_ID,HORROR_COURAGE_INC_LOC)
                    courage_mod += int([int(entry[1]) for entry in item_effect_table if entry[0].lower()==chosen_item.lower()][0])
                    #print(courage_mod,chosen_item,item_effect) good for debugging
                elif item_effect == "Hit Chance Modifier": #Item makes it easier to hit horror
                    item_effect_table = read_sheets(CRITTER_CONFIG_ID,HORROR_CHANCE_MOD_LOC)
                    hit_chance_mod += int([int(entry[1]) for entry in item_effect_table if entry[0].lower()==chosen_item.lower()][0])-hit_chance
                    #print(hit_chance,hit_chance_mod,chosen_item,item_effect) good for debugging
                elif item_effect == "Shard Drop Chance Multiplier": #Item multiplies shard chance
                    item_effect_table = read_sheets(CRITTER_CONFIG_ID,HORROR_SHARD_MUL_LOC)
                    shard_mul = int([int(entry[1]) for entry in item_effect_table if entry[0].lower()==chosen_item.lower()][0])
                    #print(shard_mul,chosen_item,item_effect) good for debugging
            #print(base_dice,courage_mod,hit_chance,hit_chance_mod,base_hp,horror_hp_mod)
        elif (not item_used) and curse_used:
            #print("No item, but curse!") # good for debugging
            #Item was not specified, but curse was
            for chosen_curse in opt_curse_list: # For each curse passed
                curse_effect = ([entry[1] for entry in curse_list if entry[0].lower()==chosen_curse.lower()][0])
                #Find the effect of the curse
                curse_name = ([entry[0] for entry in curse_list if entry[0].lower()==chosen_curse.lower()][0])
                first_param_list.append(curse_name)
                if curse_effect == "Decrease Courage": # Curse decreases dice numbers
                    curse_effect_table = read_sheets(CRITTER_CONFIG_ID,HORROR_COURAGE_DEC_LOC)
                    courage_mod -= int([int(entry[1]) for entry in curse_effect_table if entry[0].lower()==chosen_curse.lower()][0])
                    #print(courage_mod,chosen_curse,curse_effect) good for debugging
                elif curse_effect == "Hit Chance Modifier": #Curse makes it harder to hit horror
                    curse_effect_table = read_sheets(CRITTER_CONFIG_ID,HORROR_CHANCE_MOD_LOC)
                    hit_chance_mod += int([int(entry[1]) for entry in curse_effect_table if entry[0].lower()==chosen_curse.lower()][0])-hit_chance
                    #print(hit_chance,hit_chance_mod,chosen_curse,curse_effect) good for debugging
                elif curse_effect == "Horror HP Increase": #Curse increases horror HP
                    curse_effect_table = read_sheets(CRITTER_CONFIG_ID,HORROR_HP_INC_LOC)
                    horror_hp_mod += int([int(entry[1]) for entry in curse_effect_table if entry[0].lower()==chosen_curse.lower()][0])
                    #print(horror_hp_mod,chosen_curse,curse_effect) good for debugging
        elif item_used and (not curse_used):
            #Item was specified, but curse was not
            #print("Item, but no curse!") #good for debugging
            for chosen_item in opt_item_list: # For each item passed
                item_effect = ([entry[1] for entry in item_list if entry[0].lower()==chosen_item.lower()][0])
                #Find the effect of the item
                item_name_full = ([entry[0] for entry in item_list if entry[0].lower()==chosen_item.lower()][0])
                first_param_list.append(item_name_full)
                if item_effect == "Increase Courage":# Item increases dice numbers
                    item_effect_table = read_sheets(CRITTER_CONFIG_ID,HORROR_COURAGE_INC_LOC)
                    courage_mod += int([int(entry[1]) for entry in item_effect_table if entry[0].lower()==chosen_item.lower()][0])
                    #print(courage_mod,chosen_item,item_effect) good for debugging
                elif item_effect == "Hit Chance Modifier": #Item makes it easier to hit horror
                    item_effect_table = read_sheets(CRITTER_CONFIG_ID,HORROR_CHANCE_MOD_LOC)
                    hit_chance_mod += int([int(entry[1]) for entry in item_effect_table if entry[0].lower()==chosen_item.lower()][0])-hit_chance
                    #print(hit_chance,hit_chance_mod,chosen_item,item_effect) good for debugging
                elif item_effect == "Shard Drop Chance Multiplier": #Item multiplies shard chance
                    item_effect_table = read_sheets(CRITTER_CONFIG_ID,HORROR_SHARD_MUL_LOC)
                    shard_mul = int([int(entry[1]) for entry in item_effect_table if entry[0].lower()==chosen_item.lower()][0])
                    #print(shard_mul,chosen_item,item_effect) good for debugging
        hit_cnt = 0
        # Give feedback to user to demonstrate horror type and base hp
        full_horror_text = (horror_challenge_text % (horror_type,base_hp+horror_hp_mod))
        if not banished: #If you would not banish the horror
            # Calculate probablility of success
            p_succ = 1 - binom_cdf(base_hp+horror_hp_mod-1,base_dice+courage_mod,1-((hit_chance+hit_chance_mod-1)/6))
            p_succ_perc = "{0:.4f}%".format(p_succ*100) #convert probability to percent string
            full_horror_type = horror_hp_table[horrors.index(horror_type.lower())][0]
            full_courage_level = courage_table[courages.index(courage_level.lower())][0].upper()
            #print(hit_chance_mod,horror_hp_mod,courage_mod) #good for debugging
            if item_used and curse_used:
                odds_add_text = (first_odds_calc % stringify_list(sec_param_list)) + (sec_odds_calc % stringify_list(first_param_list))
            elif item_used or curse_used:
                odds_add_text = (first_odds_calc % stringify_list(first_param_list))
            else:
                odds_add_text = ""
            odds_full_text = (horr_odds_calc % (full_courage_level,full_horror_type,odds_add_text,p_succ_perc))
            odds_embed=discord.Embed(title="",description=odds_full_text, color=function_pink)
            odds_embed.set_author(name="Horror Encounter Simulated", icon_url=dice_icon)
            await ctx.send(embed=odds_embed)
        else: # You auto-dunk the horror
            odds_embed=discord.Embed(title="",description=banish_odds_text, color=function_pink)
            odds_embed.set_author(name="Certified Dunk", icon_url=dice_icon)
            await ctx.send(embed=odds_embed)
            return
    else:
        await ctx.send(embed=send_maintenance_msg())

# INVESTIGATE COMMAND PAGE 5 COMMAND 1
@commands.has_any_role("Interns","Mods","Dev")
@bot.command(name='investigate',ignore_extra=False) #User investigates a specified location (with an optional item)
async def critter_investigate(ctx,location_name,opt_item_or_curse='NULL',sec_item_or_curse='NULL'):
    global maintenance #maintenance check
    error = False
    if maintenance:
        # Load the possible investigation rooms to validate input
        critter_db_tabs = tab_list_sheets(CRITTER_CONFIG_ID)
        investigation_rooms = Diff(critter_db_tabs,non_inv_tabs)
        rooms = [room.lower() for room in investigation_rooms]
        if not location_name.lower() in rooms: # If we got a bad room as an arg
            arg_txt = find_args(ctx.message.content)
            await ctx.send(embed=send_error_msg("Error: Invalid Argument",(wrong_argument % arg_txt)))
            error = True
        else:
            # Load in useful info from sheets (room info, investigation config, special encounter chance)
            room_ind = rooms.index(location_name.lower())
            inv_info = read_sheets(CRITTER_CONFIG_ID,INV_CONFIG_LOC)
            room_info = read_sheets(CRITTER_CONFIG_ID,investigation_rooms[room_ind]+INV_ROOM_RANGE)
            special_encounter_prob = read_sheets(CRITTER_CONFIG_ID,SPECIAL_ENCOUNTER_LOC)[0]
        if opt_item_or_curse == 'NULL': # Investigation with no item or curse
            if error:
                return
            # Roll for special encounter
            if random.randint(1,100) <= int(special_encounter_prob[0]):
                if special_encounter(investigation_rooms[room_ind]):
                    await ctx.send(embed=special_encounter(investigation_rooms[room_ind]))
                    return
            roll = random.randint(1,100) #Roll a percentage for investigation
            inv_prob = inv_info[1][2:] #Grab the default probabilities since no item
            ind = 0
            for ind in range(len(inv_prob)): #Identify the found thinf range based on roll
                roll -= int(inv_prob[ind])
                if roll <= 0: #Leave to not taint index
                    break
            found = inv_info[0][ind+2] #Grab just the options to choose between
            find = run_investigation(found,room_info) #Choose the "reward"
            if find == "nothing":
                invest_embed=discord.Embed(title="",description=(exploration_results_text_nothing % (location_name,find)), color=inv_purple)
            else:
                invest_embed=discord.Embed(title="",description=(exploration_results_text % (location_name,find)), color=inv_purple)
            invest_embed.set_author(name="Exploration Results", icon_url=investigate_icon)
            await ctx.send(embed=invest_embed)
        else: # We have an agument for an item
            if sec_item_or_curse == "NULL":
                match = -1 # For validating the passed item
                for entry in inv_info: # If the item can be used to investigate
                    if entry[0].lower() == opt_item_or_curse.lower():
                        match = inv_info.index(entry)
                if match < 0: # Match wasn't changed so item is invalid
                    await ctx.send(embed=send_error_msg("Error: Invalid Item",invalid_inv_item % opt_item_or_curse))
                    return
                if error:
                    return
                # Roll for special encounter
                if random.randint(1,100) <= int(special_encounter_prob[0]):
                    if special_encounter(investigation_rooms[room_ind]):
                        await ctx.send(embed=special_encounter(investigation_rooms[room_ind]))
                        return
                inv_prob = inv_info[match][2:] # Set the probabilities for the item
                if not inv_prob[1][0].isdigit(): # Check to see if item forces a horror
                    if str(inv_prob[1]) == "H":
                        find = "a Horror"
                    elif str(inv_prob[1]) == "GH":
                        find = "a Greater Horror"
                    elif str(inv_prob[1]) == "DH":
                        find = "a Dire Horror"
                    invest_embed=discord.Embed(title="",description=(exploration_results_text % (location_name,find)), color=inv_purple)
                    invest_embed.set_author(name="Exploration Results", icon_url=investigate_icon)
                    await ctx.send(embed=invest_embed)
                    return
                roll = random.randint(10,1000)/10 #Roll a percentage for investigation
                for ind in range(len(inv_prob)): #Identify the found thinf range based on roll
                    roll -= float(inv_prob[ind])
                    if roll <= 0: #Leave to not taint index
                        break
                found = inv_info[0][ind+2] #Grab just the options to choose between
                find = run_investigation(found,room_info) #Choose the reward
                if find == "nothing":
                    invest_embed=discord.Embed(title="",description=(exploration_results_text_nothing % (location_name,find)), color=inv_purple)
                else:
                    invest_embed=discord.Embed(title="",description=(exploration_results_text % (location_name,find)), color=inv_purple)
                invest_embed.set_author(name="Exploration Results", icon_url=investigate_icon)
                await ctx.send(embed=invest_embed)
            else:
                match = [-1,-1] # For validating the passed item
                for entry in inv_info: # If the item can be used to investigate
                    if entry[0].lower() == opt_item_or_curse.lower():
                        match[0] = inv_info.index(entry)
                    if entry[0].lower() == sec_item_or_curse.lower():
                        match[1] = inv_info.index(entry)
                if match[0] == -1: # Match wasn't changed so item is invalid
                    await ctx.send(embed=send_error_msg("Error: Invalid Item",invalid_inv_item % opt_item_or_curse))
                    error = True
                if match[1] == -1: # Match wasn't changed so item is invalid
                    await ctx.send(embed=send_error_msg("Error: Invalid Curse",invalid_inv_curse % sec_item_or_curse))
                    error = True
                if inv_info[match[0]][1] == inv_info[match[1]][1]:
                    #Can only use max of 1 item and 1 curse
                    await ctx.send(embed=send_error_msg("Error: Doubles Clause",item_or_curse_text))
                    error = True
                if error:
                    return
                # Roll for special encounter
                if random.randint(1,100) <= int(special_encounter_prob[0]):
                    if special_encounter(investigation_rooms[room_ind]):
                        await ctx.send(embed=special_encounter(investigation_rooms[room_ind]))
                        return
                inf_prob_a = inv_info[match[0]][2:] #Set probabilities for first item/curse
                inf_prob_b = inv_info[match[1]][2:] # Set probabilities for 2nd item/curse
                if (not inf_prob_a[1][0].isdigit()) or (not inf_prob_b[1][0].isdigit()):
                    # Check to see if item or curse forces a horror
                    if str(inf_prob_a[1]) == "H" or str(inf_prob_b[1]) == "H":
                        find = "a Horror"
                    elif str(inf_prob_a[1]) == "GH" or str(inf_prob_b[1]) == "GH":
                        find = "a Greater Horror"
                    elif str(inf_prob_a[1]) == "DH" or str(inf_prob_b[1]) == "DH":
                        find = "a Dire Horror"
                    invest_embed=discord.Embed(title="",description=(exploration_results_text % (location_name,find)), color=inv_purple)
                    invest_embed.set_author(name="Exploration Results", icon_url=investigate_icon)
                    await ctx.send(embed=invest_embed)
                    return
                inv_prob = mix_probs(inf_prob_a,inf_prob_b) # Set the probabilities for the item
                #print(inv_prob,inf_prob_a,inf_prob_b) good for debugging
                roll = random.randint(10,1000)/10 #Roll a percentage for investigation
                ind = 0
                for ind in range(len(inv_prob)): #Identify the found thinf range based on roll
                    roll -= float(inv_prob[ind])
                    if roll <= 0: #Leave to not taint index
                        break
                found = inv_info[0][ind+2] #Grab just the options to choose between
                find = run_investigation(found,room_info) #Choose the reward
                if find == "nothing":
                    invest_embed=discord.Embed(title="",description=(exploration_results_text_nothing % (location_name,find)), color=inv_purple)
                else:
                    invest_embed=discord.Embed(title="",description=(exploration_results_text % (location_name,find)), color=inv_purple)
                invest_embed.set_author(name="Exploration Results", icon_url=investigate_icon)
                await ctx.send(embed=invest_embed)
    else:
        await ctx.send(embed=send_maintenance_msg())

# HORROR COMMAND PAGE 5 COMMAND 2
@commands.has_any_role("Interns","Mods","Dev")
@bot.command(name='horror',ignore_extra=False) #User fights a horror of specified type
async def critter_horror(ctx,horror_type,courage_level,opt_item_or_curse="",optional_curse=""):
    global maintenance #maintenance check
    error = False
    if maintenance:
        victory = False # If the user wins against the horror
        banished = False # If the user banishes the horror
        item_used = False # If the user uses item(s)
        curse_used = False # If the user uses curse(s)
        # Loads in optional item(s) and/or curse(s) as comma separated lists
        param_1_list = [elem.strip().lower().replace("’","'") for elem in opt_item_or_curse.split(",")]
        param_2_list = [elem.strip().lower().replace("’","'") for elem in optional_curse.split(",")]
        #print(param_1_list,param_2_list) # good for debugging
        if param_2_list != ['']:
            opt_item_list = param_1_list
            opt_curse_list = param_2_list
            item_used = True
            curse_used = True
        elif param_1_list[0][:5] == "curse":
            opt_item_list = []
            opt_curse_list = param_1_list
            curse_used = True
        elif param_1_list != ['']:
            opt_item_list = param_1_list
            opt_curse_list = []
            item_used = True
        else:
            opt_item_list = param_1_list
            opt_curse_list = param_2_list
        #print(item_used,curse_used) # good for debugging
        # Sorts argument lists to check compatibility
        opt_item_list.sort()
        opt_curse_list.sort()
        # Load in possible items and curses
        item_list = read_sheets(CRITTER_CONFIG_ID,HORROR_OPT_ITEM_LOC)
        curse_list = read_sheets(CRITTER_CONFIG_ID,HORROR_OPT_CURSE_LOC)
        # Grab "lowercase versions" to ensure maximum compatibility with args
        items = [entry[0].lower() for entry in item_list]
        curses = [entry[0].lower() for entry in curse_list]
        for ind in range(len(opt_item_list)):
            # Check argument viability (valid and compatible items)
            if not (opt_item_list[ind].lower() in items or opt_item_list[ind] == ''):
                await ctx.send(embed=send_error_msg("Error: Invalid Item",invalid_horr_item % opt_item_list[ind]))
                error = True
            else:
                if ind < len(opt_item_list)-1: # Items of the same set are incompatible
                    if opt_item_list[ind][:4] == opt_item_list[ind+1][:4]:
                        await ctx.send(embed=send_error_msg("Error: Invalid Argument",incompat_horr_item))
                        error = True
        for ind in range(len(opt_curse_list)):
            # Check argument viability (valid and compatible curses)
            if not (opt_curse_list[ind]== "" or opt_curse_list[ind].lower() in curses):
                await ctx.send(embed=send_error_msg("Error: Invalid Curse",invalid_curse % opt_curse_list[ind]))
                error = True
            else:
                if ind < len(opt_curse_list)-1: # Curses of the same type are incompatible
                    if opt_curse_list[ind][:12] == opt_curse_list[ind+1][:12]:
                        await ctx.send(embed=send_error_msg("Error: Incompatible Curses",incompat_horr_curse))
                        error = True
        #print("Lists examined; all compatible!") # good for debugging
        # Load in role info (hit chance, courage dice and horror hp)
        hit_chance = read_sheets(CRITTER_CONFIG_ID,HORROR_CHANCE_LOC)[0]
        hit_chance = int(hit_chance[0])
        courage_table = read_sheets(CRITTER_CONFIG_ID,HORROR_COURAGE_LOC)
        courages = [entry[0].lower() for entry in courage_table] # Courage levels used to match arg
        horror_hp_table = read_sheets(CRITTER_CONFIG_ID,HORROR_HP_LOC)
        horrors = [entry[0].lower() for entry in horror_hp_table] # Horror types used to match arg
        if not horror_type.lower() in horrors: # Check horror type arg viability
            await ctx.send(embed=send_error_msg("Error: Invalid Argument",invalid_horror_type))
            error = True
        if not courage_level.lower() in courages: # Check courage level arg viability
            await ctx.send(embed=send_error_msg("Error: Invalid Argument",invalid_courage_level))
            error = True
        #print("Horror type and courage level proved valid!") # good for debugging
        # Load in the reward/curse sheet data for rolling at the end
        item_rewards = read_sheets(CRITTER_CONFIG_ID,HORROR_ITEM_WIN_LOC)
        shard_rewards = read_sheets(CRITTER_CONFIG_ID,HORROR_SHARD_LOC)
        curse_penalty = read_sheets(CRITTER_CONFIG_ID,HORROR_CURSE_LOC)
        # Determine the dice and HP values based on args
        if error:
            return
        base_dice = int([int(entry[1]) for entry in courage_table if entry[0]==courage_level.lower()][0])
        base_hp = int([int(entry[1]) for entry in horror_hp_table if entry[0].lower()==horror_type.lower()][0])
        if "banishing sigil" in opt_item_list: #If you banished the horror bypass some stuff
            banished = True
        # Initialize modifiers for item/curse modification
        hit_chance_mod = 0
        courage_mod = 0
        horror_hp_mod = 0
        shard_mul = 1
        #print("Determined HP and initialized modifiers!") # good for debugging
        if item_used and curse_used:
            #Item and curse specified
            #print("Item and curse!") #good for debugging
            for chosen_curse in opt_curse_list: # For each curse passed
                #Find the effect of the curse
                curse_effect = ([entry[1] for entry in curse_list if entry[0].lower()==chosen_curse.lower()][0])
                if curse_effect == "Decrease Courage": # Curse decreases dice numbers
                    curse_effect_table = read_sheets(CRITTER_CONFIG_ID,HORROR_COURAGE_DEC_LOC)
                    courage_mod -= int([int(entry[1]) for entry in curse_effect_table if entry[0].lower()==chosen_curse.lower()][0])
                    #print(courage_mod,chosen_curse,curse_effect) good for debugging
                elif curse_effect == "Hit Chance Modifier": #Curse makes it harder to hit horror
                    curse_effect_table = read_sheets(CRITTER_CONFIG_ID,HORROR_CHANCE_MOD_LOC)
                    hit_chance_mod += int([int(entry[1]) for entry in curse_effect_table if entry[0].lower()==chosen_curse.lower()][0])-hit_chance
                    #print(hit_chance,hit_chance_mod,chosen_curse,curse_effect) good for debugging
                elif curse_effect == "Horror HP Increase": #Curse increases horror HP
                    curse_effect_table = read_sheets(CRITTER_CONFIG_ID,HORROR_HP_INC_LOC)
                    horror_hp_mod += int([int(entry[1]) for entry in curse_effect_table if entry[0].lower()==chosen_curse.lower()][0])
                    #print(horror_hp_mod,chosen_curse,curse_effect) good for debugging
            for chosen_item in opt_item_list: #For each item passed
                item_effect = ([entry[1] for entry in item_list if entry[0].lower()==chosen_item.lower()][0])
                #Find the effect of the item
                if item_effect == "Increase Courage":# Item increases dice numbers
                    item_effect_table = read_sheets(CRITTER_CONFIG_ID,HORROR_COURAGE_INC_LOC)
                    courage_mod += int([int(entry[1]) for entry in item_effect_table if entry[0].lower()==chosen_item.lower()][0])
                    #print(courage_mod,chosen_item,item_effect) good for debugging
                elif item_effect == "Hit Chance Modifier": #Item makes it easier to hit horror
                    item_effect_table = read_sheets(CRITTER_CONFIG_ID,HORROR_CHANCE_MOD_LOC)
                    hit_chance_mod += int([int(entry[1]) for entry in item_effect_table if entry[0].lower()==chosen_item.lower()][0])-hit_chance
                    #print(hit_chance,hit_chance_mod,chosen_item,item_effect) good for debugging
                elif item_effect == "Shard Drop Chance Multiplier": #Item multiplies shard chance
                    item_effect_table = read_sheets(CRITTER_CONFIG_ID,HORROR_SHARD_MUL_LOC)
                    shard_mul = int([int(entry[1]) for entry in item_effect_table if entry[0].lower()==chosen_item.lower()][0])
                    #print(shard_mul,chosen_item,item_effect) good for debugging
            #print(base_dice,courage_mod,hit_chance,hit_chance_mod,base_hp,horror_hp_mod)
        elif (not item_used) and curse_used:
            #print("No item, but curse!") # good for debugging
            #Item was not specified, but curse was
            for chosen_curse in opt_curse_list: # For each curse passed
                curse_effect = ([entry[1] for entry in curse_list if entry[0].lower()==chosen_curse.lower()][0])
                #Find the effect of the curse
                if curse_effect == "Decrease Courage": # Curse decreases dice numbers
                    curse_effect_table = read_sheets(CRITTER_CONFIG_ID,HORROR_COURAGE_DEC_LOC)
                    courage_mod -= int([int(entry[1]) for entry in curse_effect_table if entry[0].lower()==chosen_curse.lower()][0])
                    #print(courage_mod,chosen_curse,curse_effect) good for debugging
                elif curse_effect == "Hit Chance Modifier": #Curse makes it harder to hit horror
                    curse_effect_table = read_sheets(CRITTER_CONFIG_ID,HORROR_CHANCE_MOD_LOC)
                    hit_chance_mod += int([int(entry[1]) for entry in curse_effect_table if entry[0].lower()==chosen_curse.lower()][0])-hit_chance
                    #print(hit_chance,hit_chance_mod,chosen_curse,curse_effect) good for debugging
                elif curse_effect == "Horror HP Increase": #Curse increases horror HP
                    curse_effect_table = read_sheets(CRITTER_CONFIG_ID,HORROR_HP_INC_LOC)
                    horror_hp_mod += int([int(entry[1]) for entry in curse_effect_table if entry[0].lower()==chosen_curse.lower()][0])
                    #print(horror_hp_mod,chosen_curse,curse_effect) good for debugging
        elif item_used and (not curse_used):
            #Item was specified, but curse was not
            #print("Item, but no curse!") #good for debugging
            for chosen_item in opt_item_list: # For each item passed
                item_effect = ([entry[1] for entry in item_list if entry[0].lower()==chosen_item.lower()][0])
                #Find the effect of the item
                if item_effect == "Increase Courage":# Item increases dice numbers
                    item_effect_table = read_sheets(CRITTER_CONFIG_ID,HORROR_COURAGE_INC_LOC)
                    courage_mod += int([int(entry[1]) for entry in item_effect_table if entry[0].lower()==chosen_item.lower()][0])
                    #print(courage_mod,chosen_item,item_effect) good for debugging
                elif item_effect == "Hit Chance Modifier": #Item makes it easier to hit horror
                    item_effect_table = read_sheets(CRITTER_CONFIG_ID,HORROR_CHANCE_MOD_LOC)
                    hit_chance_mod += int([int(entry[1]) for entry in item_effect_table if entry[0].lower()==chosen_item.lower()][0])-hit_chance
                    #print(hit_chance,hit_chance_mod,chosen_item,item_effect) good for debugging
                elif item_effect == "Shard Drop Chance Multiplier": #Item multiplies shard chance
                    item_effect_table = read_sheets(CRITTER_CONFIG_ID,HORROR_SHARD_MUL_LOC)
                    shard_mul = int([int(entry[1]) for entry in item_effect_table if entry[0].lower()==chosen_item.lower()][0])
                    #print(shard_mul,chosen_item,item_effect) good for debugging
        hit_cnt = 0
        # Give feedback to user to demonstrate horror type and base hp
        full_horror_text = (horror_challenge_text % (horror_type,base_hp+horror_hp_mod))
        if not banished: #If you did not banish the horror
            for ind in range(base_dice+courage_mod): #Roll courage dice +- items/curses
                if random.randint(1,6) >= hit_chance+hit_chance_mod:
                    # If dice reaches hit chance thresh +- items/curses count a hit
                    hit_cnt += 1
            if hit_cnt >= base_hp+horror_hp_mod:
                # If enough hits to reach HP you win (+- items/curses)
                full_horror_text += (horror_victory_text % (hit_cnt,horror_type))
                rewards = roll_rewards(item_rewards,shard_rewards,horror_type,shard_mul) #roll rewards
                full_horror_text += rewards
                horror_embed=discord.Embed(title="",description=full_horror_text, color=success_green)
                horror_embed.set_author(name="Victory", icon_url=trophy_icon)
                await ctx.send(embed=horror_embed)
                return
            else:
                # If you didn't land enough hits, you lose
                full_horror_text += (horror_failure_text % (horror_type,hit_cnt))
                rewards = roll_curses(curse_penalty,horror_type) #roll a curse
                full_horror_text += rewards
                horror_embed=discord.Embed(title="",description=full_horror_text, color=reject_red)
                horror_embed.set_author(name="Defeat", icon_url=defeat_icon)
                await ctx.send(embed=horror_embed)
                return
        else: # You banished the horror
            full_horror_text += (banish_horr_text %horror_type)
            rewards = roll_rewards(item_rewards,shard_rewards,horror_type,shard_mul) #roll rewards
            full_horror_text += rewards
            horror_embed=discord.Embed(title="",description=full_horror_text, color=success_green)
            horror_embed.set_author(name="Victory", icon_url=trophy_icon)
            await ctx.send(embed=horror_embed)
            return
    else:
        await ctx.send(embed=send_maintenance_msg())

# CURSE COMMAND PAGE 5 COMMAND 3
#Needs a lot of formatting work
@commands.has_any_role("Interns","Mods","Dev")
@bot.command(name='curse',ignore_extra=False) #Re-roll curse that came from horror of specified type
async def critter_curse(ctx,*,horror_type):
    global maintenance #maintenance check
    if maintenance:
        #CHECK HORROR TYPE
        curse_penalty = read_sheets(CRITTER_CONFIG_ID,HORROR_CURSE_LOC)
        valid_horror_types = [entry[0].lower() for entry in curse_penalty]
        if not horror_type.replace('"','').replace("'","").lower() in valid_horror_types:
            await ctx.send(embed=send_error_msg("Error: Invalid Argument",invalid_horror_type))
            return
        rolled_curse = roll_curses(curse_penalty,horror_type.replace('"','').replace("'",""),1)
        curse_embed=discord.Embed(title="",description=rolled_curse, color=function_pink)
        curse_embed.set_author(name="Curse Reroll", icon_url=dice_icon)
        await ctx.send(embed=curse_embed)
    else:
        await ctx.send(embed=send_maintenance_msg())

# RAID COMMAND PAGE 5 COMMAND 4
@commands.has_any_role("Interns","Mods","Dev")
@bot.command(name="raid",ignore_extra=False)
async def raid(ctx,courage_level,opt_arg_1='',opt_arg_2=''):
    global maintenance
    error = False
    if maintenance:
        bless_used = False # If the user uses item(s)
        curse_used = False # If the user uses curse(s)
        # Loads in optional item(s) and/or curse(s) as comma separated lists
        param_1_list = [elem.strip().lower() for elem in opt_arg_1.split(",")]
        param_2_list = [elem.strip().lower() for elem in opt_arg_2.split(",")]
        #print(param_1_list,param_2_list) # good for debugging
        if param_2_list != ['']: #If I have both parameters
            if param_1_list[0][:5] == "curse": #If the first one is curses
                #param 1 is curses, param 2 is blessings
                opt_bless_list = param_2_list
                opt_curse_list = param_1_list
            else: #If the first one is blessings
                #param 1 is blessings, param 2 is curses
                opt_bless_list = param_1_list
                opt_curse_list = param_2_list
            # both blessings and curses are used
            bless_used = True
            curse_used = True
        elif param_1_list[0][:5] == "curse": #Only curses are used
            opt_bless_list = []
            opt_curse_list = param_1_list
            curse_used = True
        elif param_1_list != ['']: #Only blessings are used
            opt_bless_list = param_1_list
            opt_curse_list = []
            bless_used = True
        else: #Neither is used but lists still have to be initialized
            opt_bless_list = param_1_list
            opt_curse_list = param_2_list
        #print(bless_used,curse_used) # good for debugging
        # Sorts argument lists to check compatibility
        opt_bless_list.sort()
        opt_curse_list.sort()
        # Load in possible items and curses
        bless_list = read_sheets(CRITTER_CONFIG_ID,RAID_OPT_BLESS_LOC)
        curse_list = read_sheets(CRITTER_CONFIG_ID,RAID_OPT_CURSE_LOC)
        # Grab "lowercase versions" to ensure maximum compatibility with args
        blessings = [entry[0].lower() for entry in bless_list]
        curses = [entry[0].lower() for entry in curse_list]
        for ind in range(len(opt_curse_list)):
            # Check argument viability (valid and compatible curses)
            if not (opt_curse_list[ind]== "" or opt_curse_list[ind].lower() in curses):
                await ctx.send(embed=send_error_msg("Error: Invalid Curse",invalid_curse % opt_curse_list[ind]))
                error = True
            else:
                if ind < len(opt_curse_list)-1: # Curses of the same type are incompatible
                    if opt_curse_list[ind][:12].lower() == opt_curse_list[ind+1][:12].lower():
                        await ctx.send(embed=send_error_msg("Error: Incompatible Curses",incompat_horr_curse))
                        error = True
        #print("Lists examined; all compatible!") # good for debugging
        # Load in role info (hit chance, courage dice)
        hit_chance = read_sheets(CRITTER_CONFIG_ID,RAID_CHANCE_LOC)[0]
        hit_chance = int(hit_chance[0])
        courage_table = read_sheets(CRITTER_CONFIG_ID,RAID_COURAGE_LOC)
        courages = [entry[0].lower() for entry in courage_table] # Courage levels used to match arg
        if not courage_level.lower() in courages: # Check courage level arg viability
            await ctx.send(embed=send_error_msg("Error: Invalid Argument",invalid_courage_level))
            error = True
        for ind in range(len(opt_bless_list)):
            # Check argument viability (valid and compatible blessings)
            if not (opt_bless_list[ind].lower() in blessings or opt_bless_list[ind] == ''):
                await ctx.send(embed=send_error_msg("Error: Invalid Blessing",invalid_raid_bless % opt_bless_list[ind]))
                error = True
            else:
                if opt_bless_list[ind].lower() in blessings:
                    true_bless_i = bless_list[blessings.index(opt_bless_list[ind].lower())]
                    if true_bless_i[1] == "PD Multiplier":
                        pd_bless_str = str(true_bless_i[0])
                    for jnd in range(len(opt_bless_list)):
                        if ind != jnd:
                            true_bless_j = bless_list[blessings.index(opt_bless_list[jnd].lower())]
                            if true_bless_i[1] == true_bless_j[1]:
                                await ctx.send(embed=send_error_msg("Error: Incompatible Blessings",incompat_raid_bless))
                                return
        #print("Courage level proved valid!") # good for debugging
        # Determine the dice values based on args
        base_dice = int([int(entry[1]) for entry in courage_table if entry[0]==courage_level.lower()][0])
        # Initialize modifiers for item/curse modification
        hit_chance_mod = 0
        courage_mod = 0
        pd_mul = 1.0
        if error:
            return
        pd_blesses = []
        #print("Determined base dice and initialized modifiers!") # good for debugging
        if bless_used and curse_used:
            #Blessing and Curse specified
            #print("Blessing and Curse!") #good for debugging
            for chosen_curse in opt_curse_list: # For each curse passed
                #Find the effect of the curse
                curse_effect = ([entry[1] for entry in curse_list if entry[0].lower()==chosen_curse.lower()][0])
                if curse_effect == "Decrease Courage": # Curse decreases dice numbers
                    curse_effect_table = read_sheets(CRITTER_CONFIG_ID,RAID_COURAGE_DEC_LOC)
                    courage_mod -= int([int(entry[1]) for entry in curse_effect_table if entry[0].lower()==chosen_curse.lower()][0])
                    #print(courage_mod,chosen_curse,curse_effect) good for debugging
                elif curse_effect == "Hit Chance Modifier": #Curse makes it harder to hit horror
                    curse_effect_table = read_sheets(CRITTER_CONFIG_ID,RAID_CHANCE_MOD_LOC)
                    hit_chance_mod += int([int(entry[1]) for entry in curse_effect_table if entry[0].lower()==chosen_curse.lower()][0])-hit_chance
                    #print(hit_chance,hit_chance_mod,chosen_curse,curse_effect) good for debugging
            for chosen_bless in opt_bless_list: #For each blessing passed
                bless_effect = ([entry[1] for entry in bless_list if entry[0].lower()==chosen_bless.lower()][0])
                #Find the effect of the blessing
                if bless_effect == "Increase Courage":# Blessing increases dice numbers
                    bless_effect_table = read_sheets(CRITTER_CONFIG_ID,RAID_COURAGE_INC_LOC)
                    courage_mod += int([int(entry[1]) for entry in bless_effect_table if entry[0].lower()==chosen_bless.lower()][0])
                    #print(courage_mod,chosen_item,item_effect) good for debugging
                elif bless_effect == "Hit Chance Modifier": #Blessing makes it easier to hit horror
                    bless_effect_table = read_sheets(CRITTER_CONFIG_ID,RAID_CHANCE_MOD_LOC)
                    hit_chance_mod += int([int(entry[1]) for entry in bless_effect_table if entry[0].lower()==chosen_bless.lower()][0])-hit_chance
                    #print(hit_chance,hit_chance_mod,chosen_item,item_effect) good for debugging
                elif bless_effect == "PD Multiplier": #Blessing multiplies PD rewards
                    pd_blesses.append(chosen_bless)
                    bless_effect_table = read_sheets(CRITTER_CONFIG_ID,RAID_PD_MUL_LOC)
                    pd_mul = pd_mul * float([float(entry[1]) for entry in bless_effect_table if entry[0].lower()==chosen_bless.lower()][0])
                    #print(shard_mul,chosen_item,item_effect) good for debugging
            #print(base_dice,courage_mod,hit_chance,hit_chance_mod,base_hp,horror_hp_mod)
        elif (not bless_used) and curse_used:
            #print("No blessing, but curse!") # good for debugging
            #Blessing was not specified, but curse was
            for chosen_curse in opt_curse_list: # For each curse passed
                curse_effect = ([entry[1] for entry in curse_list if entry[0].lower()==chosen_curse.lower()][0])
                #Find the effect of the curse
                if curse_effect == "Decrease Courage": # Curse decreases dice numbers
                    curse_effect_table = read_sheets(CRITTER_CONFIG_ID,RAID_COURAGE_DEC_LOC)
                    courage_mod -= int([int(entry[1]) for entry in curse_effect_table if entry[0].lower()==chosen_curse.lower()][0])
                    #print(courage_mod,chosen_curse,curse_effect) good for debugging
                elif curse_effect == "Hit Chance Modifier": #Curse makes it harder to hit horror
                    curse_effect_table = read_sheets(CRITTER_CONFIG_ID,RAID_CHANCE_MOD_LOC)
                    hit_chance_mod += int([int(entry[1]) for entry in curse_effect_table if entry[0].lower()==chosen_curse.lower()][0])-hit_chance
                    #print(hit_chance,hit_chance_mod,chosen_curse,curse_effect) good for debugging
        elif bless_used and (not curse_used):
            #Blessing was specified, but curse was not
            #print("Blessing, but no Curse!") #good for debugging
            for chosen_bless in opt_bless_list: #For each blessing passed
                bless_effect = ([entry[1] for entry in bless_list if entry[0].lower()==chosen_bless.lower()][0])
                #Find the effect of the blessing
                if bless_effect == "Increase Courage":# Blessing increases dice numbers
                    bless_effect_table = read_sheets(CRITTER_CONFIG_ID,RAID_COURAGE_INC_LOC)
                    courage_mod += int([int(entry[1]) for entry in bless_effect_table if entry[0].lower()==chosen_bless.lower()][0])
                    #print(courage_mod,chosen_item,item_effect) good for debugging
                elif bless_effect == "Hit Chance Modifier": #Blessing makes it easier to hit horror
                    bless_effect_table = read_sheets(CRITTER_CONFIG_ID,RAID_CHANCE_MOD_LOC)
                    hit_chance_mod += int([int(entry[1]) for entry in bless_effect_table if entry[0].lower()==chosen_bless.lower()][0])-hit_chance
                    #print(hit_chance,hit_chance_mod,chosen_item,item_effect) good for debugging
                elif bless_effect == "PD Multiplier": #Blessing multiplies PD rewards
                    bless_effect_table = read_sheets(CRITTER_CONFIG_ID,RAID_PD_MUL_LOC)
                    pd_mul = pd_mul * float([float(entry[1]) for entry in bless_effect_table if entry[0].lower()==chosen_bless.lower()][0])
                    #print(shard_mul,chosen_item,item_effect) good for debugging
        hit_cnt = 0
        # Give feedback to user to demonstrate raid
        for ind in range(base_dice+courage_mod): #Roll courage dice +- items/curses
            if random.randint(1,6) >= hit_chance+hit_chance_mod:
                # If dice reaches hit chance thresh +- items/curses count a hit
                hit_cnt += 1
        # Build the embed to output the results of the raid rolls
        raid_full_text = (raid_challenge_text % (base_dice+courage_mod))
        raid_full_text += '\n\n'+(raid_complete_text % (hit_cnt))
        if pd_mul > 1:
            raid_full_text += '\n\n'+(raid_pd_mul_text % (pd_bless_str,pd_mul))
        raid_embed=discord.Embed(title="",description=raid_full_text, color=function_pink)
        raid_embed.set_author(name="Raid Damage Roll", icon_url=dice_icon)
        await ctx.send(embed=raid_embed)
    else:
        await ctx.send(embed=send_maintenance_msg())

# HATCH COMMAND PAGE 6 COMMAND 1
@commands.has_any_role("Interns","Mods","Dev")
@bot.command(name='hatch',ignore_extra=False) #Hatch a specified number of eggs (optionally fusions or color swap)
async def critter_hatch(ctx,egg_num,*,other_args=""):
    global maintenance #maintenance check
    error = False
    if maintenance:
        # Grab the list of pokemon and shiny chance from Critter DB
        pokemon_list = read_sheets(CRITTER_CONFIG_ID,HATCH_LOC)
        pokemon_types = read_sheets(CRITTER_CONFIG_ID,POKE_TYPES_LOC)
        shiny_chance = read_sheets(CRITTER_CONFIG_ID,SHINY_LOC)[0]
        shiny_chance = shiny_chance[0]
        # Default values for "special" kinds of eggs
        delta = False
        patterned = False
        color_swapped = False
        fusion = False
        # Check to ensure that the arguments are correct
        if egg_num.isdigit(): # Need Number of Eggs to hatch
            if int(egg_num) <= 0: # Number has to be positive
                await ctx.send(embed=send_error_msg("Error: Invalid Number of Eggs",inv_quantity_text))
                error = True
        else:
            await ctx.send(embed=send_error_msg("Error: Invalid Number of Eggs",inv_quantity_text))
            error = True
        # Gather up all the arguments from the command and validate tem
        args_list = other_args.replace("'",'').replace('"','').replace(',',' ').split(' ')
        for arg in args_list: # Ensure they all line up with viable args
            if arg.lower().strip() == "patterned":
                patterned = True
            elif arg.lower().strip() == "fusion":
                fusion = True
            elif arg.lower().strip() == "color-swapped":
                color_swapped = True
            elif arg.lower().strip() == "delta":
                delta = True
            else: # If they don't line up double check the arg exists before erroring
                if arg:
                    await ctx.send(embed=send_error_msg("Error: Invalid Argument",hatch_arg_text))
                    return
        if error: # Jump out if I had an error
            return
        max_hatches_per_embed = 18
        num_embeds = int(int(egg_num)/max_hatches_per_embed)+1
        for ind in range(num_embeds):
            hatch_full_text = hatch_intro_text # Start loading the text for the embed
            for i in range(min(int(egg_num)-(ind)*max_hatches_per_embed,max_hatches_per_embed)):
                # Do this "quantity" times (for each egg)
                # SETUP (Generic, done no matter what)
                mon_a = random.choice(pokemon_list) #Choose the first pokemon
                if random.randint(1,100) > int(shiny_chance): #Roll for basic v shiny
                    color_a = "basic "
                else:
                    color_a = "shiny "
                if fusion: #If I'm hatching a fusion
                    mon_b = random.choice(pokemon_list) #Choose the second pokemon
                    if random.randint(1,100) > int(shiny_chance): #Roll for basic v shiny
                        color_b = "basic "
                    else:
                        color_b = "shiny "
                    #Formulate output text for fusion case
                    hatch_mon = mon_a[0]+"/%s"+mon_b[0]+" fusion"
                else: #Formulate output text for non-fusion case
                    hatch_mon = mon_a[0]
                if color_swapped or delta: #If we override the chosen "color"
                    #Scrap what we already have
                    color_a = ""
                    color_b = ""
                    if delta: #Tack "delta" indicator onto the beginning
                        color_a = "Delta (%s) "+color_a
                    if color_swapped: #Tack "color-swapped" indicator onto the beginning
                        color_a = "color-swapped "+color_a
                if patterned:#Tack "patterned" indicator onto the beginning
                    color_a = "patterned "+color_a
                if delta: # If we're hatching a delta egg
                    # Grab the list of types we're not allowed to choose
                    if len(mon_a) > 3: # Pokemon A has extra off-limits types
                        mon_a_list = mon_a[1:2] + mon_a[3].replace(" ","").split(",")
                    elif len(mon_a) >2: # Pokemon A has 2 types (no off limits)
                        mon_a_list = mon_a[1:2]
                    else: # Pokemon A has 1 type (no off limits)
                        mon_a_list = [mon_a[1]]
                    delta_type_a = mon_a[1] # Start off with something off-limits
                    while delta_type_a in mon_a_list: # Generate until we have a good one
                        delta_type_a = random.choice(pokemon_types)[0]
                    if fusion: # If we're hatching a fusion we gotta do it again
                        # Grab the list of types we're not allowed to choose
                        if len(mon_b) > 3: # Pokemon B has extra off-limits types
                            mon_b_list = mon_b[1:2] + mon_b[3].replace(" ","").split(",")
                        elif len(mon_b) >2: # Pokemon B has 2 types (no off limits)
                            mon_b_list = mon_b[1:2]
                        else: # Pokemon B has 1 type (no off limits)
                            mon_b_list = [mon_b[1]]
                        delta_type_b = mon_b[1] # Start off with something off-limits
                        while delta_type_b in mon_b_list: # Generate until we have a good one
                            delta_type_b = random.choice(pokemon_types)[0]
                        delta_type_a += "/" + delta_type_b # Combine the types for output
                    color_a = (color_a % delta_type_a) # Stick the delta type in the output string
                if fusion: # If we have a fusion, have to add in the second "color"
                    hatch_mon = (hatch_mon % (color_b))
                # Add a line for this egg in the embed
                hatch_full_text += (hatch_egg_text % (color_a+hatch_mon))
            # Send the fully constructed embed
            hatch_embed=discord.Embed(title="",description=hatch_full_text,color=generic_blue)
            hatch_embed.set_author(name="...Oh?", icon_url=egg_icon)
            await ctx.send(embed=hatch_embed)
    else:
        await ctx.send(embed=send_maintenance_msg())

# GACHA COMMAND PAGE 6 COMMAND 2
#Needs a lot of work on formatting
@commands.has_any_role("Interns","Mods","Dev")
@bot.command(name='gacha',ignore_extra=False) #Roll a random Gacha when a user redeems a gacha ticket
async def critter_gacha(ctx):
    global maintenance
    if maintenance: #Maintenance check
        gacha_list = read_sheets(CRITTER_CONFIG_ID,GACHA_LOC)
        gacha_embed=discord.Embed(title="",description=(gacha_text % random.choice(gacha_list)[0]), color=gacha_color)
        gacha_embed.set_author(name="Gachapon", icon_url=gacha_icon)
        await ctx.send(embed=gacha_embed)
        #Need to format better
    else:
        await ctx.send(embed=send_maintenance_msg())

# VOUCHER COMMAND PAGE 6 COMMAND 3
@commands.has_any_role("Interns","Mods","Dev")
@bot.command(name='voucher',ignore_extra=False) #ROlls a value for a PD voucher when redeemed
async def critter_voucher(ctx,user='NULL'):
    global maintenance
    if maintenance: #Maintenance check
        #Grab voucher information (probabilities and ranges)
        voucher_info = read_sheets(CRITTER_CONFIG_ID,VOUCHER_INFO_LOC)
        voucher_prob = []
        voucher_range = []
        for entry in voucher_info:
            voucher_prob.append(entry[0])
            voucher_range.append(entry[1])
        roll = random.randint(1,100) #Roll a percentage for the voucher range
        for prob in voucher_prob: #Identify the voucher range based on roll
            roll -= int(prob)
            if roll <= 0: #Set voucher range (top and bottom) based on roll
                voucher_top = voucher_range[voucher_prob.index(prob)].split('-')[1]
                voucher_bottom = voucher_range[voucher_prob.index(prob)].split('-')[0]
                break
        PD_roll = random.randint(int(voucher_bottom),int(voucher_top)) # Roll the voucher
        if user == "NULL": #No target user, mod will add to inventory later
            voucher_embed=discord.Embed(title="",description=(voucher_text % PD_roll), color=fall_auburn)
            voucher_embed.set_author(name="Voucher", icon_url=voucher_icon)
            await ctx.send(embed=voucher_embed)
        else: #Target user specified, add this to target's inventory
            # Update the user inventory mapping by pulling sheets user data
            users_info = read_sheets(CRITTER_CONFIG_ID,USER_INFO_LOC)
            # Convert 2d Lists into 1d Lists (just pulled column data)
            user_full_names = [user[0] for user in users_info]
            user_inv_names = [user[1] for user in users_info]
            # Combines this into dictionary
            user_inventory_map = dict(zip(user_full_names,user_inv_names))
            try:
                arg_user_name = str(await bot.fetch_user(user[2:-1].replace("!",'')))
            except:
                await ctx.send(embed=send_error_msg("Error: Unknown User",unknown_user))
                return
            if arg_user_name in user_inventory_map: #If the user exists in the mapping
                # Pull down tab name, and balance for specified user
                tab_name = user_inventory_map[arg_user_name]
                pd_balance = read_sheets(SERVER_INVENTORY_DB,tab_name+PD_BAL_LOC)[0]
                pd_balance = pd_balance[0]
                # Update PD balance by adding the voucher roll
                pd_balance = int(pd_balance) + PD_roll
                # Write the updated balance to the sheet
                write_sheets(SERVER_INVENTORY_DB,tab_name+PD_BAL_LOC,pd_balance,0)
                # Write output to the chat channel w/Discord
                voucher_embed=discord.Embed(title="",description=(voucher_text % PD_roll), color=fall_auburn)
                voucher_embed.set_author(name="Voucher", icon_url=voucher_icon)
                await ctx.send(embed=voucher_embed)
            else: #Invalid user (not in the mapping)
                await ctx.send(embed=send_error_msg("Error: Member Database Error",(no_inventory_tab % arg_user_name.split('#')[0].split('#')[0]))) # Error, no inventory tab
    else:
        await ctx.send(embed=send_maintenance_msg())

# INVENTORY COMMANDS PAGE 7 COMMANDS 1,2, and 3
# are tied to INVENTORY at PAGE 2 COMMAND 1

# MAINTENANCE COMMAND PAGE 7 COMMAND 4
#Base functionality is there, but it needs proper formatting
@commands.has_any_role("Mods","Dev")
@bot.command(name='maintenance',ignore_extra=False) #Deactivates bot functionality for maintenance
async def critter_maintenance(ctx,value):
    global maintenance
    if int(value) == 1: #1 Allows commands
        maint_embed=discord.Embed(title="",description=maintenance_on_text, color=success_green)
        maint_embed.set_author(name="Beep Boop", icon_url=check_grn_icon)
        await ctx.send(embed=maint_embed)
        maintenance = int(value)
    elif int(value) == 0: #0 Disallows commands
        maint_embed=discord.Embed(title="",description=maintenance_off_text, color=success_green)
        maint_embed.set_author(name="Beep Boop", icon_url=check_grn_icon)
        await ctx.send(embed=maint_embed)
        maintenance = int(value)
    else: #Anything else is wrong
        await ctx.send(embed=send_error_msg("Error: Invalid Toggle",maintenance_wrong_text))

# INJURY COMMAND PAGE 7 COMMAND 5
#Needs a lot of formatting work
@commands.has_any_role("Mods","Dev")
@bot.command(name='injury',ignore_extra=False) #Pull random injury from sheets based on category and "give" to target
async def critter_injury(ctx,target,category):
    global maintenance
    error = False
    if maintenance: #Maintenance check
        if injury_type_decode(category) == -1: # Make sure the user passed a valid category
            await ctx.send(embed=send_error_msg("Error: Injury Type Not Found",injury_error_text))
            error = True
        # Load in tenants by nickname to validate/choose random target
        tenant_list = read_sheets(CRITTER_CONFIG_ID,TENANT_LIST)
        tenant_nicknames_lower = [tenant[1].lower() for tenant in tenant_list]
        tenant_nicknames = [tenant[1] for tenant in tenant_list]
        # Load in injuries based on injury category passed
        injury_list = read_sheets(CRITTER_CONFIG_ID,injury_type_decode(category))
        inflicted_injury = random.choice(injury_list)
        if target.lower() == 'random': #Target can be random
            chosen = random.choice(tenant_nicknames) # Pick a random tenant by nickname
        else:
            if target.lower() in tenant_nicknames_lower: # Ensure the target is a known tenant
                chosen = tenant_nicknames[tenant_nicknames_lower.index(target.lower())]
            else: # Error unkown tenant
                await ctx.send(embed=send_error_msg("Error: Tenant Not Found",unknown_tenant))
                return
        if error:
            return
        injury_embed=discord.Embed(title="",description=(injury_text % (chosen,str(inflicted_injury[0]),str(inflicted_injury[1]))), color=reject_red)
        injury_embed.set_author(name=("%s Injury Sustained" % (category[0].upper()+category[1:].lower())), icon_url=injury_icon)
        await ctx.send(embed=injury_embed)
    else:
        await ctx.send(embed=send_maintenance_msg())

# KEY COMMANDS PAGE 8 COMMANDS 1,2, and 3
#Needs a lot of formatting work
@commands.has_any_role("Mods","Dev")
@bot.command(name='key',ignore_extra=False) #Mod adds views or deletes to/from key total
async def critter_key(ctx,command_ext='NULL',user_name='NULL',quantity='0'):
    global maintenance #maintenance check
    error = False
    if maintenance:
        if command_ext.lower() == "add" or command_ext.lower() == "delete":
            if quantity.isdigit(): # Need Number for quantity
                if int(quantity) < 0: # Number has to be positive
                    await ctx.send(embed=send_error_msg("Error: Invalid Number of Keys",inv_quantity_text))
                    error = True
            else:
                await ctx.send(embed=send_error_msg("Error: Invalid Number of Keys",inv_quantity_text))
                error = True
        elif command_ext.lower() == "view":
            if quantity != '0':
                await ctx.send(embed=send_error_msg("Error: Bamboozled",too_many_args))
                error = True
        # Update the user inventory mapping by pulling sheets user data
        users_info = read_sheets(CRITTER_CONFIG_ID,USER_INFO_LOC)
        # Convert 2d Lists into 1d Lists (just pulled column data)
        user_full_names = [user[0] for user in users_info]
        user_key_total = [user[2] for user in users_info]
        if command_ext.lower() == 'add': # Add quantity keys to user_name's total
            if user_name == 'NULL' or quantity == '0': # Argument verification
                arg_txt = "username or key quantity"
                await ctx.send(embed=send_error_msg("Error: Missing Argument",(missed_argument % arg_txt)))
                return
            try:
                arg_user_name = str(await bot.fetch_user(user_name[2:-1].replace("!",'')))
            except:
                await ctx.send(embed=send_error_msg("Error: Unknown User",unknown_user))
                return
            if arg_user_name in user_full_names: # If the user exists in the mapping
                if error:
                    return
                key_embed = discord.Embed(title="",description=(key_add_text % (user_name,quantity)),color=success_green)
                key_embed.set_author(name="Addition Successful", icon_url=check_grn_icon)
                await ctx.send(embed=key_embed)
                # Load key total of user
                user_keys = int(user_key_total[user_full_names.index(arg_user_name)])
                user_keys += int(quantity) # Add quantity keys
                # Store in info array to write back to sheets later
                users_info[user_full_names.index(arg_user_name)][2] = user_keys
            else: #Invalid user (not in the mapping)
                await ctx.send(embed=send_error_msg("Error: Member Database Error",(no_inventory_tab % arg_user_name.split("#")[0])))
                return
        elif command_ext.lower() == 'delete': #Delete quantity keys from user_name's total
            if user_name == 'NULL' or quantity == '0': # Argument verification
                arg_txt = "username or key quantity"
                await ctx.send(embed=send_error_msg("Error: Missing Argument",(missed_argument % arg_txt)))
                return
            try:
                arg_user_name = str(await bot.fetch_user(user_name[2:-1].replace("!",'')))
            except:
                await ctx.send(embed=send_error_msg("Error: Unknown User",unknown_user))
                return
            if arg_user_name in user_full_names: # If the user exists in the mapping
                if error:
                    return
                # Load key total of user
                user_keys = int(user_key_total[user_full_names.index(arg_user_name)])
                if user_keys < int(quantity): # Doesn't have enough keys to delete that many
                    await ctx.send(embed=send_error_msg("Error: Insufficient Keys",(not_enough_keys % (user_name,user_keys))))
                    return
                user_keys -= int(quantity) # Remove quantity keys
                # Store in info array to write back to sheets later
                users_info[user_full_names.index(arg_user_name)][2] = user_keys
                key_embed = discord.Embed(title="",description=(key_delete_text % (quantity,user_name)),color=success_green)
                key_embed.set_author(name="Removal Successful", icon_url=check_grn_icon)
                await ctx.send(embed=key_embed)
            else: #Invalid user (not in the mapping)
                await ctx.send(embed=send_error_msg("Error: Member Database Error",(no_inventory_tab % arg_user_name.split("#")[0])))
                return
        elif command_ext.lower() == 'view': # View the key total of user_name
            if user_name == 'NULL': # Argument verification
                arg_txt = "username"
                await ctx.send(embed=send_error_msg("Error: Missing Argument",(missed_argument % arg_txt)))
                return
            try:
                arg_user_name = str(await bot.fetch_user(user_name[2:-1].replace("!",'')))
            except:
                await ctx.send(embed=send_error_msg("Error: Unknown User",unknown_user))
                return
            if arg_user_name in user_full_names: # If the user exists in the mapping
                if error:
                    return
                # Load key total of user
                user_keys = int(user_key_total[user_full_names.index(arg_user_name)])
                key_embed = discord.Embed(title="",description=(key_view_text % (user_name,user_keys)),color=success_green)
                key_embed.set_author(name="Key Amount", icon_url=check_grn_icon)
                await ctx.send(embed=key_embed)
                return
            else: #Invalid user (not in the mapping)
                await ctx.send(embed=send_error_msg("Error: Member Database Error",(no_inventory_tab % arg_user_name.split("#")[0])))
                return
        else:
            await ctx.send(embed=send_error_msg("Error: Command Error",invalid_command))
            return
        # Write (potentially) updated array back to user key total
        write_sheets(CRITTER_CONFIG_ID,USER_INFO_LOC,users_info)
    else:
        await ctx.send(embed=send_maintenance_msg())

# COMMS COMMAND PAGE 8 COMMAND 4
@commands.has_any_role("Mods","Dev")
@bot.command(name='comms',ignore_extra=False) #Mod adds views or deletes to/from key total
async def critter_comms(ctx,chan_or_ann,*,extra_text=""):
    global maintenance #maintenance check
    if maintenance:
        if chan_or_ann.lower() == "birthday" or chan_or_ann.lower() == "birthdays":
            channel = bot.get_channel(BIRTHDAY_CHAN)
            birthdays = check_birthdays()
            print(len(birthdays))
            if len(birthdays) != 0:
                birth_txt = ""
                for name in birthdays.keys():
                    birth_txt += (birthday_text % (name,birthdays[name]))
                if len(birthdays) == 1:
                    print("I think 1 birthday")
                    birth_embed=discord.Embed(title="",description=belated_text+one_birthday_text+birth_txt, color=generic_blue)
                else:
                    print("I think many birthdays!")
                    birth_embed=discord.Embed(title="",description=belated_text+many_birthday_text+birth_txt, color=generic_blue)
                birth_embed.set_author(name="Happy Birthday to You", icon_url=birthday_icon)
                birth_embed.set_footer(text=birth_footer_text)
                await channel.send(embed=birth_embed)
                await channel.send(target_birthdays_grp)
                return
        elif chan_or_ann.lower() == "investigation" or chan_or_ann.lower() == "investigations":
            channel = bot.get_channel(INVESTIGATE_CHAN)
            ann_embed=discord.Embed(title="",description=belated_text+investigations_open_text, color=inv_purple)
            ann_embed.set_author(name="Time for Adventure", icon_url=investigate_icon)
            await channel.send(embed=ann_embed)
            await channel.send(target_investigators_grp)
            return
        elif chan_or_ann.lower() == "season" or chan_or_ann.lower() == "seasons":
            channel = bot.get_channel(SEASON_CHAN)
            await channel.send(embed=season_change(check_season()))
            return
        else:
            try:
                channel = bot.get_channel(int(chan_or_ann[2:-1]))
            except:
                await ctx.send(embed=send_error_msg("Error: Unknown Channel/Announcement Type",inv_ann_or_chan))
            await channel.send(extra_text)
    else:
        await ctx.send(embed=send_maintenance_msg())

# ERROR EVENTS (COMMAND NOT FOUND, MISSING ARGUMENT, MISSING ROLE, OTHER)
@bot.event
async def on_command_error(ctx, error): #Handles any command errors
    if isinstance(error, discord.ext.commands.errors.CommandNotFound): #Command not found
        await ctx.send(embed=send_error_msg("Error: Command Error",invalid_command))
    elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument): #Missing an argument
        arg_txt=find_args(ctx.message.content)
        await ctx.send(embed=send_error_msg("Error: Missing Argument",(missed_argument % arg_txt)))
    elif isinstance(error, discord.ext.commands.MissingAnyRole): #Missing some number of roles
        await ctx.send(embed=send_error_msg("Error: Invalid Permissions",no_permission))
    elif isinstance(error, discord.ext.commands.MissingRole): #Missing specific role
        await ctx.send(embed=send_error_msg("Error: Invalid Permissions",no_permission))
    elif isinstance(error, discord.ext.commands.TooManyArguments): #Too many args
        await ctx.send(embed=send_error_msg("Error: Bamboozled",too_many_args))
    elif isinstance(error, discord.ext.commands.ExpectedClosingQuoteError): #Expected Closing Quote
        await ctx.send(embed=send_error_msg("Error: Consistent Quotes Required",expect_closing_quote))
    elif isinstance(error, discord.ext.commands.NoPrivateMessage):
        await ctx.send(embed=send_error_msg("Error: I'm Out of My Element",out_of_element_txt))
    else: #Anything else is unlikely, but problematic
    # Once deployed, change this to write to some sort of log file
        await ctx.send(embed=send_error_msg("Error: Something Went Wrong",serious_error))
        error_string = "Error: %s\n\n Occured when %s invoked %s."
        error_string = (error_string % (str(error),str(ctx.message.author),str(ctx.message.content)))
        dev_user = await bot.fetch_user(dev_id)
        await dev_user.create_dm()
        await dev_user.dm_channel.send(error_string)

@tasks.loop(hours=24)
async def update_timing():
    now = datetime.datetime.now()
    now = now - timedelta(hours=5)
    old_season = check_season(now)
    #print(str(now))
    tomorrow = now + timedelta(days=1)
    midnight_tomorrow = tomorrow.replace(hour=0, minute=0, second=1)
    #print(str(midnight_tomorrow))
    seconds_until = (midnight_tomorrow - now).total_seconds()

    await asyncio.sleep(seconds_until)
    #print("I woke up at "+str(datetime.datetime.now()))
    #print(midnight_tomorrow.weekday())
    #print(midnight_tomorrow.day)
    if midnight_tomorrow.day == 1:
        season = check_season(midnight_tomorrow)
        #print(season,old_season)
        if season != old_season:
            channel = bot.get_channel(SEASON_CHAN)
            await channel.send(embed=season_change(season))
            return
    if midnight_tomorrow.weekday() == 6:
        print("I think it's sunday, let's check birthdays!")
        channel = bot.get_channel(BIRTHDAY_CHAN)
        birthdays = check_birthdays()
        print(len(birthdays))
        if len(birthdays) != 0:
            birth_txt = ""
            for name in birthdays.keys():
                birth_txt += (birthday_text % (name,birthdays[name]))
            if len(birthdays) == 1:
                print("I think 1 birthday")
                birth_embed=discord.Embed(title="",description=one_birthday_text+birth_txt, color=generic_blue)
            else:
                print("I think many birthdays!")
                birth_embed=discord.Embed(title="",description=many_birthday_text+birth_txt, color=generic_blue)
            birth_embed.set_author(name="Happy Birthday to You", icon_url=birthday_icon)
            birth_embed.set_footer(text=birth_footer_text)
            await channel.send(embed=birth_embed)
            await channel.send(target_birthdays_grp)
            return
    elif (midnight_tomorrow.weekday() == 0) or (midnight_tomorrow.weekday() == 3):
        print("I think it's monday or thursday, let's announce investigations!")
        channel = bot.get_channel(INVESTIGATE_CHAN)
        ann_embed=discord.Embed(title="",description=investigations_open_text, color=inv_purple)
        ann_embed.set_author(name="Time for Adventure", icon_url=investigate_icon)
        await channel.send(embed=ann_embed)
        await channel.send(target_investigators_grp)
        return
    return

bot.run(TOKEN)
