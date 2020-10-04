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

user = {
    'user_id': None,
    'permissions_id': None,
    'last_login': None,
    'last_action': None,
    'username': None,
    'first_name': None,
    'last_name': None
}

thread = {
    'parent': None,
    'category_id': None,
    'message': None,
    'thread_id': None,
    'time': None,
    'title': None,
    'likes': None,
    'comments': []
}

comment = {
    'comment_id': None,
    'thread_id': None,
    'user_id': None,
    'message': None,
    'time': None
}

category = {
    'category_id': None,
    'name': None,
    'parent': None
}

commands = {}

menus = {}

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