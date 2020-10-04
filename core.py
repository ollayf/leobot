'''
This script contains the core functions that are required in multiple processes
Commonly used functions like getting the time, etc
'''

import datetime
from collections import defaultdict
from utils.logic import *
from utils.core_utils import *

## ADMINSTRATIVE
#################

def initiate_user(update, context):
    '''
    Set ups the important information for each user that hasn't been initiated yet
    '''

    username = update.message.from_user.username

    # for people that are not yet members in bot_data
    if not tuple(categories.data.keys()).__contains__(user_id):
        context.bot_data['members'][username] = user_id

        # sends a message to the coders when someone is initiated nbv   
        for coder in context.bot_data['coders']:
            context.bot.send_message(chat_id=coder, text=f'{user_id} added to list of members as {username} with \
permissions {context.user_data["permissions"]}.')
    
    # initiate user
    if context.user_data == {}:
        # create default user_data for this user
        set_user_data_to_default(update, context, default_user_data.copy())
        # give permissions
        context.user_data['permissions'] = get_user_permissions(user_id, context)
        # pms the person briefly about the role of alphabot
        context.bot.send_message(chat_id=update.effective_message.from_user.id, \
                        text=first_use)
        
        # initiates the username, user_id, group_id
        context.user_data['username'] = username
        context.user_data['user_id'] = user_id
        context.user_data['group_id'] = context.bot_data['chat_id']

    return result