'''
This script compiles the requirements for the bot and runs it on a loop
It should also contain the functions of the bot
'''

from config import *
from core import *
import telegram
import datetime
import time
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, \
ConversationHandler, CallbackQueryHandler
import logging
import random
from pytz import timezone
import emojis
import argparse
import utils.db_utils as db_utils
import argparse

print('initialising')
# checks if this should be run ion testing env
parser = argparse.ArgumentParser(description='Runs the leobot service')
parser.add_argument('-t', '--testing', type=bool, help='Whether you want to run in testing env')
args = parser.parse_args()
# setting up deployment environment env (REMOVE IF YOU ARE NOT USING env FILE BUT IT IS GOOD PRACTICE)
testing = args.testing
print('Testing value:', testing)
import configparser
config = configparser.ConfigParser()
config.read('bot.cfg')

if testing:
    bot_config = dict(config['test_bot'])
    print(str(config))
    dbi = db_utils.Database(config, 'test_db')
else:
    bot_config = config['live_bot']
    dbi = db_utils.Database(config, 'live_db')

# TODO: ACTUAL DEPLOYMENT CHANGE
owner = config['owners']['fei']

updater = Updater(token=bot_config['token'], use_context=True)
dispatcher = updater.dispatcher # for quicker access to the dispatcher object
jobqueuer = updater.job_queue # for quicker access to JobQueue object

# logs the problems in log.md file with level INFO
logging.basicConfig(filename='storage/error_log.txt', format='%(asctime)s - %(name)s - \
                    %(levelname)s - %(message)s', level=logging.INFO)

core_utils.setup_bot_data(dispatcher, owner, bot_config, dbi, testing)

msg_return = dispatcher.bot.send_message(owner, bot_init_msg) # informs the owners that it is intialised
print('Message Return', str(msg_return))

################
# TESTING ZONE #
################
# dbi.new_category('Testimony', des= 'Heartfelt personal sharing')
# dbi.cat_id('Testimony')

# def process_members(update, context):
#     '''
#     Processes the changes in member data i.e. when the user first starts the bot.
#     This function being in group 0 make sure it is the highest priority and runs in parallel with other
#     callback functions
#     '''
#     # for easier access to user_id
#     user_id = update.message.from_user.id

#     # initiates the user if it is his first time
#     initiate_user(user_id, update, context) # in utils

#     # updates the permission according to quits by the coder
#     # check_for_personal_changes(update, context)

# dispatcher.add_handler(MessageHandler(Filters.text, process_members), group=0) # gives most prirority
new_thread_conv = ConversationHandler(
    entry_points=[CommandHandler('new_thread', new_thread)],
    states={
        TITLE: [MessageHandler(Filters.text & ~Filters.command, t_title)],
        CAT: [MessageHandler(Filters.text & ~Filters.command, t_cat)],
        BODY: [MessageHandler(Filters.text & ~Filters.command, t_body)],
        FILE: [core_utils.file_handler(t_file),
                CommandHandler('no', t_file)],
        TAGS: [MessageHandler(Filters.text & ~Filters.command, t_tags)],
        TC: [MessageHandler(Filters.text & ~Filters.command, tc_next)]

    },
    fallbacks= [CommandHandler('cancel', cancel),
                CommandHandler('end', end)],
    map_to_parent= {
        COMPLETED: MENU,
        END: END,
        CANCEL: MENU
    }
)

feedback_conv = ConversationHandler(
    entry_points=[CommandHandler('feedback', fb_init)],
    states={
        TITLE: [MessageHandler(Filters.text & ~Filters.command, \
            fb_title)],
        BODY: [MessageHandler(Filters.text & ~Filters.command, fb_body)],
        FILE: [core_utils.file_handler(fb_file),
                CommandHandler('no', fb_file)]
    },
    fallbacks= [CommandHandler('cancel', cancel),
                CommandHandler('end', end)],
    map_to_parent= {
        COMPLETED: MENU,
        END: END,
        CANCEL: MENU
    }
)

admin_conv = ConversationHandler(
    entry_points=[CommandHandler('admin_menu', admin_menu)],
    states={
        MENU: [CommandHandler('sview_fb', sview_fb),
            CommandHandler('dview_fb', dview_fb),
            CommandHandler('ch_perm', ch_perm),
            CommandHandler('all_members', all_members),
            CommandHandler('del_threads', del_threads)
            ],
    },
    fallbacks= [CommandHandler('quit', quit_m),
                CommandHandler('end', end)],
    map_to_parent= {
        END: END,
        QUIT: MENU
    }
)

be_conv = ConversationHandler(
    entry_points=[CommandHandler('backend', admin_menu)],
    states={
        MENU: [],
    },
    fallbacks= [CommandHandler('quit', quit_m),
                CommandHandler('end', end)],
    map_to_parent= {
        END: END,
        QUIT: MENU
    }
)

start_conv = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        MENU: [
            new_thread_conv,
            feedback_conv,
            admin_conv,
            ],
        END: [CommandHandler('start', start)],
        TIMEOUT: [MessageHandler(Filters.text, timeout)]
    },
    fallbacks= [CommandHandler('end', end)],
    conversation_timeout=600
)

# def not_command(update, context):
#     '''
#     Processes messages that are not commands i.e. a response to a prompt by the bot
#     Make sure this is the last callback function to grant lowest priority to because this means that 
#     the person is clearly not trying to call another function
#     '''
#     update.message.reply_text('Not real command')

# dispatcher.add_handler(MessageHandler(Filters.command, not_command), group=1)
dispatcher.add_handler(CommandHandler('help', help_fns))
dispatcher.add_handler(CommandHandler('cache', cache))
dispatcher.add_handler(start_conv)

def remind_events(context):
    # TODO: Make bot record events and remind people
    inform_owners(daily_msg, context)

event_reminder = jobqueuer.run_daily(callback=remind_events,\
    time=datetime.time(8, 0, 0, 0, tzinfo=timezone('Singapore')))

updater.start_polling()
dbi.close()
