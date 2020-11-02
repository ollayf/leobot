import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, \
    CallbackQueryHandler, ConversationHandler, Filters
import logging
from leo_msgs import template_1
from utils.core_utils import get_msg_file, post_thread

API_TOKEN = '1171777871:AAGvfNQU6fvV1P8X970YBjT9m4ewfBFhITk'
logging.basicConfig(filename='storage/error_log.txt', format='%(asctime)s - %(name)s - \
                    %(levelname)s - %(message)s', level=logging.INFO)
# FOR CREATING THREAD
NEW_THREAD, \
TITLE, \
CAT, \
BODY, \
FILE, \
TAGS = map(chr, range(10, 16))

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
INVALID, \
MENU = map(chr, range(9))

# SPECIFIC COMMANDS:
FEEDBACK = chr(20)

def new_thread(update, context):
    context.user_data['new_thread'] = True
    update.message.reply_text('sup title?')
    return TITLE

def t_title(update, context):
    reply = update.message.text
    context.user_data['title'] = reply
    update.message.reply_text('sup cat?')
    return CAT

def t_cat(update, context):

    reply = update.message.text
    context.user_data['cat'] = reply
    update.message.reply_text('What is the main message of the post?')
    return BODY

def t_body(update, context):

    reply = update.message.text
    context.user_data['body'] = reply
    update.message.reply_text('WHAT PHOTO /no if you dont want photo')
    return FILE

def t_file(update, context):
    context.user_data['file_id'], context.user_data['file_type'],= \
        get_msg_file(update.message)
    update.message.reply_text('What TAGS? (split by commas)')
    return TAGS

def t_tags(update, context):
    reply = update.message.text
    context.user_data['tags'] = [reply, 'potato']
    update.message.reply_text('thanks for your submission')
    content = prepare_thread(context)
    post_thread(update, context, content)
    return COMPLETED

def prepare_thread(context):
    thread_id = 1
    category = context.user_data['cat']
    title = context.user_data['title']
    body = context.user_data['body']
    tags = ', '.join(context.user_data['tags'])
    content = template_1.format(thread_id=thread_id, category=category, \
                                title=title, body=body, tags=tags)
    return content

# ***** FOR CREATING THREADS *****
    
def start(update, context):
    update.message.reply_text(text='STARTED')
    return MENU

def cancel(update, context):
    update.message.reply_text('cancelling job')
    return CANCEL

def end(update, context):
    update.message.reply_text('ending conversation')
    return END

def quit(update, context):
    update.message.reply_text('quiting all menus and resetting data')
    return QUIT

def bot_print(update, context):
    print('here')
    update.message.reply_text('YEETED')
    return MENU

def timeout(update, context):
    update.message.reply_text('Sorry bruh your session has timed out.. please start \
a new conversation with me')

def feedback_start(update, context):
    update.message.reply_text('wut feedback')
    return FEEDBACK

def feedback_complete(update, context):
    msg = update.message.text
    print(msg)
    username = update.message.from_user.username
    print(username)
    feedback = f"""Feedback from {username}:
{msg}"""
    print('here1')
    context.bot.send_message(333647246, feedback)
    print('here2')
    update.message.reply_text('tenk for feedback bruh')
    return END

def no(update, context):
    update.message.reply_text('no photo taken')
    return NO

def yes(update, context):
    return YES

def invalid(update, context):
    update.message.reply_text('INVALID INPUT')
    return INVALID

updater = Updater(API_TOKEN, use_context=True)

# Get the dispatcher to register handlers
dp = updater.dispatcher
msg_return = dp.bot.send_message(333647246, 'test')

new_thread_conv = ConversationHandler(
    entry_points=[CommandHandler('new_thread', new_thread)],
    states={
        TITLE: [MessageHandler(Filters.text & ~Filters.command, t_title)],
        CAT: [MessageHandler(Filters.text & ~Filters.command, t_cat)],
        BODY: [MessageHandler(Filters.text & ~Filters.command, t_body)],
        FILE: [MessageHandler(Filters.photo | Filters.document \
            | Filters.video | Filters.audio | Filters.voice, t_file)
& ~Filters.command, t_file),
                CommandHandler('no', t_file)],
        NO: [MessageHandler(Filters.text & ~Filters.command, t_tags)],
        TAGS: [MessageHandler(Filters.text & ~Filters.command, t_tags)]

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
    entry_points=[CommandHandler('feedback', feedback_start)],
    states={
        FEEDBACK: [MessageHandler(Filters.text & ~Filters.command, feedback_complete)]
    },
    fallbacks= [CommandHandler('cancel', cancel),
                CommandHandler('end', end)],
    map_to_parent= {
        COMPLETED: MENU,
        END: END,
        CANCEL: MENU
    }
)

start_conv = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        MENU: [
            new_thread_conv,
            feedback_conv],
        END: [CommandHandler('start', start)],
        TIMEOUT: [MessageHandler(Filters.text, timeout)]
    },
    fallbacks= [CommandHandler('end', end)],
    conversation_timeout=900

)
# for test sending docs
def doc(update, context):
    msg = update.message
    print(str(msg.document))
    update.message.reply_text(str(msg.document))
dp.add_handler(CommandHandler('doc', doc))


dp.add_handler(start_conv)
dp.add_handler(CommandHandler('bot_print', bot_print))
updater.start_polling()