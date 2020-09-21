'''
This script contains all the usual messages such as:
- Error messages
- Intiialising messages
- Successful action messages

It also links to all the relative paths
'''

########################
# DEFAULT SETUP CONFIG #
########################

# TODO: What is displayed when asked for the info of the bot
BOT_DESCRIPTION = ''

# TODO: Edit according to what we need to keep etc. This is initialised for each user when they become a member
default_user_data = {
'username': None,
'user_id': None,
'group_id': None,
'permissions': None,
'status': {
    # for members
    'initiated': False, 'started': False, 'feedback': False, 'action': False,
    # for cfm IC
    'cfm_settings': False, 'change_msg': 0,
    # for admins
    'admin_menu': False, 'add_event': 0, 'add_teaching': 0,
    # for coders
    'backend': False
    },
'temp_list': [],
'temp_string' : ''
}

##################
# ERROR MESSAGES #
##################

# TODO: I USED THIS TO MAKE ENDING THE BOT SLIGHTLY MORE INTERESTING
fail_end_msgs = ['Wait bruh we aren\'t even in a conversation...',\
    'Uhm ok... It\'s not like i wanted to talk to you anyway',\
    'Wait whats there to end? Wait end me?!! Why do you want to end me?!'
    ]

not_started_error = 'Hello... Please start a conversation with me first with /start'
not_integer_error = 'Value is not an integer. Try inputting index again'
out_of_range_error = 'Index out of range'
one_arg_error = 'Only 1 argument allowed to be input'
not_exist_error = 'this person does not exist'
cancel_fail = 'You are not currently in an action!'
permission_fail = 'You have no power here!'
function_fail = 'This function is not allowed in the mode you have activated. E.G. admin_menu'
quit_fail = 'bruh there\'s nothing to quit lol'
user_timeout_msg = '15 minutes is up, I will automatically be going to sleep. Please remember \
to end the conversation when not in use.\nYou can also use /events, /library, /start_call \
/end_call without starting me up.'

######################
# SUCCESSFUL ACTIONS #
######################

cancel_msg = 'Alrighty! Action cancelled!'

# I USED THIS TO MAKE ENDING THE BOT SLIGHTLY MORE INTERESTING (a message is randomly selecting when 
# the user ends the session)
end_msgs = ['Going so soon...._Alright..._Bye then...',\
    'Alright come back soon ok? :D',\
    'Don\'t go, I\'m lonely...',\
    'Have nice day',\
    'Thank you for waiting._We\'ve restored your Pokémon to full health._We hope to see you again!',\
    'k thx bai'
    ]

# when a user initialises the bot for the first time
first_start_msg = 'Welcome {}! Is this your first time? Hi my name is ALPHAbot. I store important \
information and do particular administrative tasks to aide the running of LG. However just \
like you I am not perfect, so please do not hesitate to give me feedback on how I can serve you \
and the LG better. You can use \n/feedback to give me your feedback\n\n\
\
Commands you can use without doing /start (for quick use):\n\
/events -- shows the list of upcoming events including their dates, timings and locations.\n\
/library -- shows the list of good articles/ sermons to read in you own time.\n\
/start_call -- to be called when you start a call on any platform (only available for admins)\n\
/end_call -- ends the call that is currently on (only available for admins)\n\
/birthdays -- shows the full list of birthdays as well as the closest birthday.\n\
/help -- can be used at any time to give the list of possible functions'

# 
quit_fin_msg = 'Thanks bro. Goodbye!'

# This is currently how I create the menu when i /help. TBH there could be a cleaner way to do this, i just
possible_commands = {
    'sleep' : { # the default mode
        'events': 'shows the list of upcoming events',
        'library': 'opens up a library of recent good teachings and articles',
        'patch_notes': 'Shows the patch notes of the last update',
        'info': 'Find out more about me and what I do!',
        'start': 'start a conversation with me :)',
        'part1': 'ONLY AVAILABLE FOR ADMINS',
        'start_call': '/start_call [url] to start a call. \
Sends a message to the group that the call is on, don\'t say bojio.',
        'end_call': 'Informs me that the call is ended, aka stopping the spam',
        'base_menu': ''
        },

    'started' : { # the mode activated after /start
        'events': 'shows the list of upcoming events',
        'library': 'opens up a library of recent good teachings and articles',
        'patch_notes': 'Shows the patch notes of the last update',
        'info': 'Find out more about me and what I do!',
        'feedback': 'opens up the floor for a good ol\' one sided roasting session. Come at me bro',
        'part1': 'FOR ADMINS ONLY',
        'start_call': '/start_call [url] to start a call.\
Sends a message to the group that the call is on, don\'t say bojio.',
        'end_call': 'Informs me that the call is ended, aka stopping the spam',
        'admin_menu': 'Opens the menu of functions for admins',
        'cfm_settings': 'Opens the menu of functions for the confirmation IC',
        'bday_settings': 'Opens the menu of functions for the birthday IC',
        'end': 'ends the conversation with me :(',
        'base_menu': ''
        }
    }