'''
This script compiles the requirements for the bot and runs it on a loop
It should also contain the functions of the bot
'''


import telegram
import datetime
import time
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, PicklePersistence
import logging
import random
from pytz import timezone
import emojis
import argparse

updater = Updater(token=live_token, use_context=True)
dispatcher = updater.dispatcher # for quicker access to the dispatcher object
jobqueuer = updater.job_queue # for quicker access to JobQueue object

#TODO: THIS IS WHERE THE LIST OF FUNCTIONS WILL BE
# Important keywords:
# start - starting a conversation with the bot
# cancel - the act of cancelling an action when the user is in the middle of one
# quit - the act of leaving a menu to return to the start (or main) menu
# end - opposite of starting, aka ending the conversation with bot, all memory is cleared

updater.start_polling()