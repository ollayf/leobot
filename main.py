'''
This script compiles the requirements for the bot and runs it on a loop
It should also contain the functions of the bot
'''

from leo_msgs import *
from utils.core_utils import *
from utils.logic import *
from config import *
from tables.table_classes import Table
import telegram
import datetime
import time
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import random
from pytz import timezone
import emojis
import argparse

print('initialised')

# setting up deployment environment env (REMOVE IF YOU ARE NOT USING env FILE BUT IT IS GOOD PRACTICE)
testing = True

import configparser
env = configparser.ConfigParser()
env.read('bots.cfg')

if testing:
    deploy_env = env['testing']
else:
    deploy_env = env['live']

updater = Updater(token=deploy_env['token'], use_context=True)
dispatcher = updater.dispatcher # for quicker access to the dispatcher object
jobqueuer = updater.job_queue # for quicker access to JobQueue object

owner = env['owners']['fei']
chat = deploy_env['chat_id']

# logs the problems in log.md file with level INFO
logging.basicConfig(filename='storage/error_log.txt', format='%(asctime)s - %(name)s - \
                    %(levelname)s - %(message)s', level=logging.INFO)

# SETUP DATABASE
# categories = Table('categories')
# comments = Table('comments')
# permissions = Table('permissions')
# threads = Table('threads')
# users = Table('users')

msg_return = dispatcher.bot.send_message(owner, bot_init_msg) # informs the owners that it is intialised
print('Message Return', str(msg_return))

def process_members(update, context):
    '''
    Processes the changes in member data i.e. when the user first starts the bot.
    This function being in group 0 make sure it is the highest priority and runs in parallel with other
    callback functions
    '''
    # for easier access to user_id
    user_id = update.message.from_user.id

    # initiates the user if it is his first time
    initiate_user(user_id, update, context) # in utils

    # updates the permission according to quits by the coder
    # check_for_personal_changes(update, context)

dispatcher.add_handler(MessageHandler(Filters.text, process_members), group=0) # gives most prirority

def post(update, context):
    '''
    Processes messages that are not commands i.e. a response to a prompt by the bot
    Make sure this is the last callback function to grant lowest priority to because this means that 
    the person is clearly not trying to call another function
    '''
    text = '''
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. In dolor ligula, dapibus sed faucibus non, aliquam ac ipsum. Sed dictum tincidunt scelerisque. Integer tristique sollicitudin augue a sollicitudin. Morbi ipsum ante, tempus sit amet velit vel, dictum mattis velit. Pellentesque porttitor cursus tortor, sit amet pharetra massa laoreet vitae. Praesent nulla ante, mollis sit amet mattis vel, venenatis sit amet nibh. In non massa in lacus eleifend interdum. Aliquam nec ipsum sed mi finibus ornare eu quis lorem. Duis orci est, imperdiet quis nisl non, aliquam efficitur ex. Nunc viverra nulla libero. Phasellus mattis euismod est, non pretium massa fringilla ac. Suspendisse gravida posuere mi id finibus. Pellentesque sed metus vitae nisl tincidunt ultricies nec eget ante. Vestibulum venenatis felis ante, nec pellentesque nisi accumsan non. Morbi nulla lacus, iaculis id tincidunt tincidunt, tempor et risus.
    '''
    context.bot.send_message(chat, text=text)

dispatcher.add_handler(CommandHandler('post', post), group=1)

def process_msg(update, context):
    '''
    Processes messages that are not commands i.e. a response to a prompt by the bot
    Make sure this is the last callback function to grant lowest priority to because this means that 
    the person is clearly not trying to call another function
    '''
    pass

dispatcher.add_handler(MessageHandler(Filters.text, process_msg), group=1)

#TODO: THIS IS WHERE THE LIST OF FUNCTIONS WILL BE
# Important keywords:
# start - starting a conversation with the bot
# cancel - the act of cancelling an action when the user is in the middle of one
# quit - the act of leaving a menu to return to the start (or main) menu
# end - opposite of starting, aka ending the conversation with bot, all memory is cleared

updater.start_polling()
updater.idle()