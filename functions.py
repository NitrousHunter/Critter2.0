#!/usr/bin/env python3
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow,Flow
from google.auth.transport.requests import Request
import os
import pickle
import discord
import random
import datetime
import itertools as it
from discord.ext import commands

from string_dec import *

def get_commands(page_num):
# Gets the proper dictionary of "Help" commands based on the page number
    if (page_num == 1):
        return help_dict_1
    elif (page_num == 2):
        return help_dict_2
    elif (page_num == 3):
        return help_dict_3
    elif (page_num == 4):
        return help_dict_4
    elif (page_num == 5):
        return help_dict_5
    elif (page_num == 6):
        return help_dict_6
    elif (page_num == 7):
        return help_dict_7
    elif (page_num == 8):
        return help_dict_8
    else:
        print("ERROR: HELP IS ONLY 7 PAGES")
        return -1


def find_args(function):
# Gets the argument names based on the function name (gets from context)
    fun_name = function[2:].split(' ')[0]
    if(fun_name == "suggest"):
        args_text = 'suggestion text'
    elif(fun_name == "bug"):
        args_text = 'report text'
    elif(fun_name == "buy"):
        args_text = 'item name or quantity'
    elif(fun_name == "sell"):
        args_text = 'item name or quantity'
    elif(fun_name == "gift"):
        args_text = 'recipient name, item name or quantity'
    elif(fun_name == "exchange"):
        args_text = 'shards quantity'
    elif(fun_name == "join"):
        args_text = 'role name'
    elif(fun_name == "leave"):
        args_text = 'role name'
    elif(fun_name == "investigate"):
        args_text = 'location name'
    elif(fun_name == "horror"):
        args_text = 'horror type or courage level'
    elif(fun_name == "curse"):
        args_text = 'horror type'
    elif(fun_name == "hatch"):
        args_text = 'number of eggs'
    elif(fun_name == "maintenance"):
        args_text = 'maintenance number'
    elif(fun_name == "injury"):
        args_text = 'tenant name or injury category'
    elif(fun_name == "info"):
        args_text = 'item(s), blessing(s), or curse(s) name(s)'
    else:
        args_text = " ERROR "
    return args_text

def shop_page_decode(page_num):
# Gets the proper location of Shop items in the sheet based on the page number
    if page_num == 1:
        return SHOP_PAGE1
    elif page_num == 2:
        return SHOP_PAGE2
    elif page_num == 3:
        return SHOP_PAGE3
    elif page_num == 4:
        return SHOP_PAGE4
    elif page_num == 5:
        return SHOP_PAGE5
    elif page_num == 6:
        return SHOP_PAGE6
    elif page_num == 7:
        return SHOP_PAGE7
    elif page_num == 8:
        return SHOP_PAGE8
    else:
        return -1

def injury_type_decode(injury_type):
# Gets the proper location of injuries in the sheet based on the injury type
    if injury_type.lower() == "minor":
        return INJURY_INFO_MINOR
    elif injury_type.lower() == "moderate":
        return INJURY_INFO_MODERATE
    elif injury_type.lower() == "severe":
        return INJURY_INFO_SEVERE
    elif injury_type.lower() == "critical":
        return INJURY_INFO_CRITICAL
    elif injury_type.lower() == "random":
        return INJURY_INFO_RANDOM
    else:
        return -1

def init_sheets():
# Initializes the connection to google sheets API. Honestly not certain exactly how it works
    global values_input, service
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

def read_sheets(SHEET_ID,RANGE):
# Reads the specified sheet at specified range and returns the value(s) as a 2d-list
    sheet = service.spreadsheets()
    result_input = sheet.values().get(spreadsheetId=SHEET_ID,
                                range=RANGE).execute()
    values_input = result_input.get('values', [])
    return values_input

def read_sheets_multiple(SHEET_ID,RANGE_LIST):
# Reads the specified sheet at specified ranges and returns the value(s) as a 2d-list
    RANGE = ";".join(RANGE_LIST)
    sheet = service.spreadsheets()
    result_input = sheet.values().batchGet(spreadsheetId=SHEET_ID,
                                ranges=RANGE_LIST).execute()
    value_ranges = result_input.get('valueRanges', [])
    values = [range.get('values',[]) for range in value_ranges]
    flat_values = [item for sublist in values for item in sublist]
    return flat_values

def write_sheets(SHEET_ID,RANGE,DATA,DATA_DIM = 2):
# Writes the specified data to the cells in the specified range of the specified sheet
# Need to include "dimension" of the data because sheets API needs 2d list
    if DATA_DIM == 2:
        VALUE = DATA
    elif DATA_DIM == 1:
        VALUE = [DATA]
    elif DATA_DIM == 0:
        VALUE = [[DATA]]
    else:
        print("What are you doing, you wrote this function moron")
    response_date = service.spreadsheets().values().update(
        spreadsheetId=SHEET_ID,
        valueInputOption='USER_ENTERED',
        range=RANGE,
        body=dict(
            majorDimension='ROWS',
            values=VALUE)
    ).execute()
    #print('Sheet successfully Updated')

def clear_sheets(SHEET_ID,RANGE):
#Clears the specified range of the specified sheets of all data
    sheet = service.spreadsheets()
    body = {}
    result_clear = sheet.values().clear(spreadsheetId=SHEET_ID,
                                range=RANGE,body=body).execute()

def tab_list_sheets(SHEET_ID):
#Grabs the list of all tab names on the specified sheet
    sheet_metadata = service.spreadsheets().get(spreadsheetId=SHEET_ID).execute()
    sheets = sheet_metadata.get('sheets', '')
    titles = [ tab_name.get("properties",{}).get("title") for tab_name in sheets]
    return titles

def Diff(li1, li2):
#Returns the items in one list but not the other
    return (list(list(set(li1)-set(li2)) + list(set(li2)-set(li1))))

def triangle_num(n):
#Computes the "triangle number" of n (I think... necessary for keys math)
    return int((n*n+n)/2)

def factorial(n): #Calculates the factorial of n
    fact = 1
    if n == 0:
        return fact
    for i in range(1,n+1):
        fact=fact*i
    return fact

def binom_cdf(k,n,p): #Calculate the binmial cdf for k, n and p
    cdf = 0
    cdf = (1-p)**n
    for x in range(1,k+1):
        prob = (factorial(n)/(factorial(x)*factorial(n-x)))*(p**x)*(1-p)**(n-x)
        cdf += prob
    if cdf > 1:
        cdf = 1
    return cdf

def stringify_list(list): # Takes list and puts them together
    if list:
        if len(list) > 1:
            list[-2] += ", and"
        if len(list) > 2:
            out_string = (", ".join(list)).replace(", and,",", and")
        else:
            out_string = (", ".join(list)).replace(", and,"," and")
    else:
        out_string = ""
    return out_string

def grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return it.zip_longest(fillvalue=fillvalue, *args)

def combine_like_entries(tuples): #Combines tuples in list if item,quantity pairs
    items = [tuple[0].lower() for tuple in tuples]
    dict = {}
    for item in items:
        tmp = []
        if items.count(item) > 1:
            tmp = [ind for ind in range(len(items)) if items[ind] == item]
            quantity = 0
            for j in range(len(tmp)-1,0,-1):
                quantity += int(tuples[tmp[j]][1])
                del tuples[tmp[j]]
                del items[tmp[j]]
            tuples[items.index(item)][1] = str(quantity+int(tuples[items.index(item)][1]))
    return(tuples)

def tablify_list(list_arg): # Takes list and puts them together
    if list_arg:
        grouped_list = list(grouper(2,list_arg,""))
        out_string = ""
        for entry in grouped_list:
            out_string += " {:28s} ║ {:28s} \n".format(entry[0],entry[1])
    else:
        out_string = ""
    return out_string

def special_encounter(room_name):
    if room_name == "Pond": #Untitled Swanna Encounter
        embed=discord.Embed(title="",description=swanna_encounter_text, color=inv_purple)
        embed.set_author(name="Untitled Swanna Encounter", icon_url=inv_event_icon)
        embed.set_image(url=swanna_image)
        return embed
    else: #Not a valid special encounter
        return False

def run_investigation(thing_found,room_information):
#Selects the actual reward found in an investigation based on the thing found and room info
    if thing_found.lower() == "special":
        # If you found a "special" choose 1 at random
        find_pool = [entry[0] for entry in room_information if entry[0] != '']
        if find_pool:
            return random.choice(find_pool)
        else:
            return -1
    elif thing_found.lower() == "horror":
        # If you found a "horror" roll to see what kind/if you encounter a horror
        find_pool = [entry[1] for entry in room_information if len(entry) > 1 and entry[1] != '']
        find_probs = [entry[2] for entry in room_information if len(entry) > 1 and entry[2] != '']
        if find_pool and find_probs:
            roll = random.randint(100,10000)/100
            for ind in range(len(find_probs)):
                roll -= float(find_probs[ind])
                if roll <= 0:
                    break
            return find_pool[ind]
        else:
            return -1
    elif thing_found.lower() == "pokemon":
        # If you found a "pokemon" choose 1 at random (account for seasons)
        season = check_season()
        find_pool = []
        for ind in range(len(room_information)):
            if(len(room_information[ind])>5):
                if(len(room_information[ind])>6):
                    find_pool.append(room_information[ind][5+season])
                else:
                    find_pool.append(room_information[ind][5])
            else:
                break
        if find_pool:
            return random.choice(find_pool)
        else:
            return -1
    elif thing_found.lower() == "item":
        # If you found an "item" roll to see what kind/if you get one
        find_pool = [entry[3] for entry in room_information if len(entry) > 3 and entry[3] != '']
        find_probs = [entry[4] for entry in room_information if len(entry) > 3 and entry[4] != '']
        if find_pool and find_probs:
            roll = random.randint(100,10000)/100
            for ind in range(len(find_probs)):
                roll -= float(find_probs[ind])
                if roll <= 0:
                    break
            return find_pool[ind]
        else:
            return -1
    elif thing_found.lower() == "nothing":
        return "nothing"
    else:
        return -1

def mix_probs(list_probs_a, list_probs_b):
    #A way of combining probability matrixes; first multiply then normalize
    #Possibly not the most efficient, but it gets the job done
    out_probs = []
    for ind in range(len(list_probs_a)):
        out_probs.append(int(list_probs_a[ind]) * int(list_probs_b[ind]))
    #print(out_probs)
    total = sum(out_probs)
    #print(total)
    for ind in range(len(out_probs)):
        out_probs[ind] = (out_probs[ind]/total)*100
    return out_probs

def roll_rewards(item_rewards,shard_rewards,horror_type,shard_mul):
#Roll rewards earned in a horror encounter
    horrors_shards = [entry[0].lower() for entry in shard_rewards]
    # pull shards information from critter db
    type_shards = horrors_shards.index(horror_type.lower()) # determine type of horror passed
    prob = shard_rewards[type_shards][1] #determine probability of shards based on horror type
    #print(horror_type,type_shards,prob) good for debugging
    if random.randint(10,1000)/10 <= float(prob)*shard_mul: #roll to see if shards obtainted
        #print("won shards")
        shard_prize_top = int(shard_rewards[type_shards][2].split('-')[1])
        shard_prize_bottom = int(shard_rewards[type_shards][2].split('-')[0])
        # Roll to see how many shards you earned
        shards = random.randint(shard_prize_bottom,shard_prize_top)
        rewards = (won_shards_text % shards)
        #print(rewards)
    else: #no shards obtained
        rewards = lost_shards_text
    horrors_item_types = [entry.lower() for entry in item_rewards[0]] #pull item info from db
    type_items = horrors_item_types.index(horror_type.lower()) #link horror type to item info
    #print(horrors_item_types,type_items)
    #print(item_rewards)
    item_pool = []
    for ind in range(len(item_rewards)): #determine item pool based on horror type
        if (len(item_rewards[ind]) > type_items) and (ind != 0):
            item_pool.append(item_rewards[ind][type_items])
    #print(item_pool)
    item_pool = list(filter(None,item_pool)) #get rid of empty list entries
    #print(item_pool,type_items,horror_type) good for debugging
    prize = random.choice(item_pool) #choose a prize
    rewards += (item_prize_text % prize)
    return rewards

def roll_curses(curse_penalty,horror_type,override=0):
#roll a curse from horror encounter (or reroll)
    horror_type_curse = [entry[0].lower() for entry in curse_penalty]
    # pull curse information from critter db
    #print(horror_type_curse) good for debugging
    type_curse = horror_type_curse.index(horror_type.lower()) # determine type of horror passed
    prob = curse_penalty[type_curse][1] #determine probability of curse based on horror type
    # print(horror_type,type_curse,prob) good for debugging
    if override: # Passing from curse command; guaranteed curse
        curses = [elem.strip() for elem in curse_penalty[type_curse][2].split(",")]
        # pull list of curses from the sheet
        curse = random.choice(curses) #pick a curse from the list
        penalty = (reroll_curse_text % (horror_type,curse))
        return penalty
    if (random.randint(1,100) <= int(prob)): # Roll to see if there is a curse
        curses = [elem.strip() for elem in curse_penalty[type_curse][2].split(",")]
        # pull list of curses from the sheet
        curse = random.choice(curses) #pick a curse from list
        penalty = (lost_curse_text % curse)
    else: # Got away safe
        penalty = lost_nothing_text
    return penalty

def check_season(currentDT = datetime.datetime.now()):
#Check the season at the specified time (now by default)
    print(str(currentDT))
    seasons = ['Spring','Summer','Fall','Winter']
    if currentDT.month in [12, 1, 2]:
        season = 3
    elif currentDT.month in [3, 4, 5]:
        season = 0
    elif currentDT.month in [6, 7, 8]:
        season = 1
    elif currentDT.month in [9, 10, 11]:
        season = 2
    else:
        season = 4
    print("It is currently %s!" % seasons[season])
    return season

def check_birthdays():
#Check who's birthday is within 1 week of today and output useful text
    currentDT = datetime.datetime.now()
    curr_weekday = currentDT.weekday()
    if curr_weekday == 6:
        curr_weekday = -1
    week_list = [currentDT + datetime.timedelta(days=x) for x in range(-1-curr_weekday,6-curr_weekday)]
    dates_list = [(str(date.month).rjust(2,'0')+'-'+str(date.day).rjust(2,'0')) for date in week_list]
    tenant_pulled_list = read_sheets(CRITTER_CONFIG_ID,TENANT_LIST)
    tenant_birthdays = [[entry[0],entry[4]] for entry in tenant_pulled_list]
    weekly_birthdays = {}
    for [name,date] in tenant_birthdays:
        if date in dates_list:
            obj_date = datetime.datetime.strptime(date,"%m-%d")
            obj_date = obj_date.replace(year=currentDT.year)
            if obj_date.month == currentDT.month and obj_date.day == currentDT.day:
                weekly_birthdays[name]="today"
            else:
                weekly_birthdays[name]=obj_date.strftime('%A, %B %d')
    return weekly_birthdays

def send_error_msg(err_name,err_text):
# Send an Error message embed with specified title and text
    err_embed=discord.Embed(title="",description=err_text, color=reject_red)
    err_embed.set_author(name=err_name, icon_url=error_icon)
    return err_embed

def send_maintenance_msg():
# Send the maintenance message embed with randomly chosen maintenance gif
    maint_embed=discord.Embed(title="",description=maintenance_block_text, color=maint_grey)
    maint_embed.set_author(name="Be Back Soon!", icon_url=maintenance_icon)
    maint_embed.set_image(url=random.choice(maintenance_images))
    return maint_embed

def season_change(season):
# Send the season change embed with different themes based on the season in question
    season_embed=discord.Embed(title="",description=season_here[season],color=season_color[season])
    season_embed.set_author(name=("%s Has Arrived" % season_name[season]),icon_url=season_icons[season])
    return season_embed
