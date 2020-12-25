default_user_data = {
'callsign': None,
'status': {
    # for members
    'initiated': False, 'started': False, 'feedback': False, 'action': False, 'thread': 0, 'comment': 0,
    # for admins
    'admin_menu': False,
    # for devs
    'backend': False
    },
'temp_list': [],
'temp_string' : ''
}

# This is currently how I create the menu when i /help. TBH there could be a cleaner way to do this, i just
commands = {
    'sleep' : { # the default mode
        # 'events': 'shows the list of upcoming events',
        'patch_notes': 'Shows the patch notes of the last update',
        'info': 'Find out more about me and what I do!',
        'start': 'start a conversation with me :)',
        'part1': 'ONLY AVAILABLE FOR ADMINS',
        'backend': 'only for devs',
        'base_menu': ''
        },

    'started' : { # the mode activated after /start
        # 'events': 'shows the list of upcoming events',
        'patch_notes': 'Shows the patch notes of the last update',
        'info': 'Find out more about me and what I do!',
        'feedback': 'Use to enter feedback to the developers',
        'new_thread': 'Starts a new thread',
        'part1': 'FOR ADMINS ONLY',
        # 'admin_menu': 'Opens the menu of functions for admins',
        'end': 'ends the conversation with me :(',
        'base_menu': ''
        }
    }

######################3
# LIST OF EVENT CODES #
#######################

# FOR CREATING THREAD
NEW_THREAD, \
TITLE, \
CAT, \
BODY, \
FILE, \
TC, \
TAGS = map(chr, range(10, 17))

# BASIC COMMANDS AT ALL POINTS

END, \
TIMEOUT = -1, -2

START, \
CANCEL, \
QUIT, \
INIT, \
COMPLETED, \
YES, \
NO, \
SELECT, \
INVALID, \
MENU = map(chr, range(10))

# selection
USER, \
PERMS = map(chr, range(30, 32))

# SPECIFIC COMMANDS:
FEEDBACK = chr(20)
