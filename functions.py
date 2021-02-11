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
