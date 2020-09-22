'''
This script compiles the requirements for the bot and runs it on a loop
It should also contain the functions of the bot
'''

from env import *
from utils import *
import telegram
import datetime
import time
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, PicklePersistence
import logging
import random
from pytz import timezone
import emojis
import argparse

print('initialised')

# setting up deployment environment config (REMOVE IF YOU ARE NOT USING CONFIG FILE BUT IT IS GOOD PRACTICE)
testing = True

import configparser
config = configparser.ConfigParser()
config.read('bots.cfg')

if testing:
    deploy_config = config['testing']
else:
    deploy_config = config['live']

updater = Updater(token=deploy_config['token'], use_context=True)
dispatcher = updater.dispatcher # for quicker access to the dispatcher object
jobqueuer = updater.job_queue # for quicker access to JobQueue object

owner = config['owners']['fei']
chat = deploy_config['chat_id']

# logs the problems in log.md file with level INFO
logging.basicConfig(filename='storage/error_log.txt', format='%(asctime)s - %(name)s - \
                    %(levelname)s - %(message)s', level=logging.INFO)

msg_return = dispatcher.bot.send_message(owner, bot_init_msg) # informs the owners that it is intialised
print(str(msg_return))

def process_members(update, context):
    '''
    Processes the changes in member data i.e. when the user first starts the bot.
    This function being in group 0 make sure it is the highest priority and runs in parallel with other
    callback functions
    '''
    pass

dispatcher.add_handler(MessageHandler(Filters.text, process_members), group=0) # gives most prirority

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