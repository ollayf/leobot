from utils.logic import *
import logging

def menu_activated(user_data):
    '''
    Checks if any menu is currently activated
    Returns True if it is and False if it isn't
    '''
    menus = ['admin_menu', 'backend', 'confirmation', 'birthday']
    status_dict = user_data['status']
    result = False
    # checks if any of the menus are accessed currently
    for menu in menus:
        # if this condition is never invoked, result will return False
        if status_dict[menu]:
            result = True

def check_permission(auth, requirement):
    '''
    Checks if the permission level of the user is sufficient for the action
    Returns True if allowed, False if not
    '''
    power_level = {
        'coders': 20,
        'admins': 10,
        'bday_IC': 2,
        'cfm_IC': 2,
        'members': 1
    }
    assert tuple(power_level.keys()).__contains__(auth), 'User Perms not exist'
    assert tuple(power_level.keys()).__contains__(requirement), 'Reqm Perms not exist'

    # to be returned
    result = False
    if auth == requirement:
        result = True
    
    elif power_level[auth] > power_level[requirement]:
        result = True

    else:
        result = False

    return result

def set_user_data_to_default(update, context, default_user_data):
    '''
    Recursively sets user_data of this user to default user_data
    '''
    assert isinstance(default_user_data, (dict, defaultdict)), \
        'default user data must be a defaultdict or dict'
    # recursively add the attributes of the dictionary
    for key in default_user_data.keys():
        # make the list or dictionary immutable
        if isinstance(default_user_data[key], (dict, list)):
            context.user_data[key] = default_user_data[key].copy()
        else:
            context.user_data[key] = default_user_data[key]

def close_all_menus(user_data):
    '''
    Closes all menus in the conversation
    If a new menu is added, change this function and the next only
    '''
    user_data['status']['admin_menu'] = False
    user_data['status']['backend'] = False
    user_data['status']['cfm_settings'] = False
    user_data['status']['bday_settings'] = False

def clear_user_memory(user_data, end=False, quit=False):
    '''
    in an event such as ending the bot, reset all the attributes of the user to default
    '''
    pass



def bot_print(update, text):
    '''
    replies a certain msg to the sender
    '''
    if type(text) != str:
        text = str(text)
    update.message.reply_text(text=text)