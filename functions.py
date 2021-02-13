#!/usr/bin/env python3
from string_dec import *

def get_commands(page_num):
    if (page_num == 1):
        return commands_dict_1
    elif (page_num == 2):
        return commands_dict_2
    elif (page_num == 3):
        return commands_dict_3
    elif (page_num == 4):
        return commands_dict_4
    elif (page_num == 5):
        return commands_dict_5
    elif (page_num == 6):
        return commands_dict_6
    else:
        print("ERROR: HELP IS ONLY 6 PAGES")
        return -1


def find_args(function):
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
    else:
        args_text = " ERROR "
    return args_text
