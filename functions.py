import utils.db_utils as db_utils
import configparser

functions = {
    # general use
    'help': ['find out what are the functions you can access now',
            0, 0,0 ,0 ,1 
            ],
    'start': ['starts a conversation with the bot',
            1, 0, 0 ,0 ,0
            ],
    'cancel': ['cancels currently using job or function',
            0, 0 ,0 ,0, 0, 1 
            ],
    'end': ['ends the conversation menu',
            0, 1, 1 ,1, 0, 1
            ],
    'quit': ['quits all menus and returns to start menu',
            0, 0, 1, 1, 0, 1
            ],
    # for start menu
    'admin_menu': ['enters the admin menu (only for people with admin perms)',
            0, 1, 0, 0, 0, 0, 5
            ],
    'new_thread': ['write a new thread to be posted in the group!',
            0, 1, 0, 0, 0, 0],
    'feedback': ['write a feedback to the admins',
            0, 1, 0, 0, 0, 0
            ],
    # for admin menu
    'sview_fb': ['Feedback Summary View',
            0, 0, 1, 0, 0, 0],
    'dview_fb': ['<feedback id> Feedback Detailed View',
            0, 0, 1, 0, 0, 0
            ],
}

if __name__ == '__main__':
    testing = True

    config = configparser.ConfigParser()
    config.read('bot.cfg')

    if testing:
        bot_config = dict(config['test_bot'])
        print(str(config))
        dbi = db_utils.Database(config, 'test_db')
    else:
        bot_config = config['live_bot']
        dbi = db_utils.Database(config, 'live_db')
    
    dbi.write_fns_table(functions)