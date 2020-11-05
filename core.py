'''
This script contains the core functions that are required in multiple processes
Commonly used functions like getting the time, etc
'''

import datetime
import telegram
from config import *
from leo_msgs import *
import utils.core_utils as core_utils
import utils.logic as logic
import random

# ***** FUNDAMENTALS *****
def cancel(update, context):
    context.user_data.clear()
    update.message.reply_text('job cancelled')
    return CANCEL

def end(update, context):
    chosen_msg = random.choice(end_msgs)
    update.message.reply_text(chosen_msg)
    context.user_data.clear()
    return END

def quit(update, context):
    update.message.reply_text('quiting all menus and resetting data')
    context.user_data.clear()
    return QUIT

def timeout(update, context):
    update.message.reply_text(timeout_msg)
    context.user_data.clear()
    return END

def no(update, context):
    return NO

def yes(update, context):
    return YES

def invalid(update, context):
    update.message.reply_text('INVALID INPUT')
    return INVALID

# ***** FOR CREATING THREADS *****
def new_thread(update, context):
    
    context.user_data['new_thread'] = True
    update.message.reply_text(t_title_msg)
    return TITLE

def t_title(update, context):
    # collect previous data
    reply = update.message.text
    context.user_data['title'] = reply
    # write choices
    dbi = context.bot_data['dbi']
    msg, cats = core_utils.prepare_cats_msg(t_cat_msg, dbi)
    context.user_data['cats'] = cats
    update.message.reply_text(msg)
    return CAT

def t_cat(update, context):
    reply = update.message.text
    dbi = context.bot_data['dbi']
    cats = context.user_data['cats']
    print('here')
    try:
        choice = core_utils.cat_choice(reply, cats)
    except:
        print('error found')
        update.message.reply_text(out_of_range_error)
        msg, _ = core_utils.prepare_cats_msg(t_cat_msg, dbi)
        update.message.reply_text(msg)
        return CAT

    context.user_data['cat'] = choice
    update.message.reply_text(t_body_msg)
    return BODY

def t_body(update, context):
    reply = update.message.text
    context.user_data['body'] = reply
    update.message.reply_text(t_file_msg)
    return FILE

def t_file(update, context):
    context.user_data['file_id'], context.user_data['file_type'] = \
        core_utils.get_msg_file(update.message)
    update.message.reply_text(t_tags_msg)
    return TAGS

def t_complete(update, context):
    # AFTER EVERYTHING IS CONFIRMED
    dbi = context.bot_data['dbi']
    author_id = update.message.from_user.id
    update.message.reply_text(t_complete_msg)
    thread_id = dbi.get_thread_id()
    content = core_utils.prepare_thread(context, template_1, thread_id)
    print('CONTENT:', content)
    # to be chnaged in deployment
    chat_id = context.bot_data['chat_id']
    print(context.user_data)
    msg = core_utils.post_thread(update, context, content, chat_id)
    print(msg)
    author_id = dbi.u_id(author_id) # gets the u_id
    core_utils.log_thread(dbi, thread_id, context, msg, author_id)
    print(str(msg))
    context.user_data.clear()
    return COMPLETED

def t_tags(update, context):
    dbi = context.bot_data['dbi']
    reply = update.message.text
    tags = core_utils.parse_tags(reply)
    print('getting cats')
    tags_ref = dbi.get_cats(tag=True)
    tags_ref = list(map(lambda x: x[0], tags_ref))
    print('creating tc')
    tc = core_utils.TagChecker(tags, tags_ref, dbi)
    context.user_data['tc'] = tc
    print('getting next elemnt')
    curr_tag = tc.next()
    print('AFTER NEXT')

    if curr_tag is None:
        return t_complete(update, context)
    else:
        update.message.reply_text(t_tagger_msg)
        qn = tc.prepare_tc_qn(t_tags_check_msg)
        update.message.reply_text(qn)
        return TC

def tc_next(update, context):
    reply = update.message.text
    tc = context.user_data['tc']
    try:
        reply = int(reply)
    except ValueError:
        update.message.reply_text(out_of_range_error)
        qn = tc.prepare_tc_qn(t_tags_check_msg)
        update.message.reply_text(qn)
        return TC
    else:
        try:
            # updates the tags
            tc.update_curr(reply)
        except KeyError:
            return TC

    next_tag = tc.next()
    if next_tag:
        print('Preparign next qn')
        qn = tc.prepare_tc_qn(t_tags_check_msg)
        update.message.reply_text(qn)
        return TC
    else:
        return t_complete(update, context)

# ***** FOR CREATING THREADS *****
    
################
# FOR FEEDBACK #
################

def fb_init(update, context):
    update.message.reply_text(fb_title_msg)
    return TITLE

def fb_title(update, context):
    reply = update.message.text
    context.user_data['title'] = reply
    update.message.reply_text(fb_details_msg)
    return BODY

def fb_body(update, context):
    reply = update.message.text
    context.user_data['body'] = reply
    update.message.reply_text(fb_file_msg)
    return FILE

def fb_file(update, context):
    msg = update.message
    file_id, file_type = core_utils.get_msg_file(msg)
    dbi = context.bot_data['dbi']
    user_id = msg.from_user.id
    author_id = dbi.u_id(user_id)
    title, body = core_utils.get_fb_details(context)
    dbi.new_fb(author_id, title, body, file_id, file_type)

    # send notification to owner
    owner = context.bot_data['owner']
    username = update.message.from_user.username
    print(username)
    feedback = f"""New Feedback from {username}"""
    context.bot.send_message(owner, feedback)
    update.message.reply_text(fb_complete_msg)
    return COMPLETED

##################
# FOR ADMIN MENU #
##################
def admin_menu(update, context):
    print('in admin menu')
    dbi = context.bot_data['dbi']
    user_id = update.message.from_user.id
    fn = 'admin_menu'
    print('checking permissions')
    if core_utils.check_permissions(fn, user_id, dbi):
        print('replying')
        username = update.message.from_user.username
        update.message.reply_text(admin_menu_msg.format(username))
        return MENU
    else:
        update.message.reply_text(permission_fail)
        return END

def sview_fb(update, context):
    dbi = context.bot_data['dbi']
    content = core_utils.sumview_fb(dbi)
    print('CONTENT:', content)
    update.message.reply_text(content, parse_mode='MarkdownV2')
    return MENU

def dview_fb(update, context):
    dbi = context.bot_data['dbi']
    args = context.args
    for arg in args:
        try:
            choice = int(arg)
        except ValueError:
            update.message.reply_text(not_integer_error)
            continue
        else:
            core_utils.detview_fb(choice, dbi, update, context)
    return MENU


def start(update, context):
    print('HERE')
    user = update.message.from_user
    user_id = user.id
    dbi = context.bot_data['dbi']
    yeet = dbi.user_exist(user_id)
    print('yeet', yeet)
    if dbi.user_exist(user_id):
        update.message.reply_text(text=start_msg)
    else:
        username = user.username
        print('got here')
        core_utils.initiate_user(dbi, user)
        update.message.reply_text(text=first_start_msg.format(username))
    return MENU

