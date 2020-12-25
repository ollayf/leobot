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
    core_utils.reset_user(context)
    core_utils.ch_menu(context, action=False)
    update.message.reply_text('job cancelled')
    return CANCEL

def end(update, context):
    chosen_msg = random.choice(end_msgs)
    core_utils.ch_menu(context, 'sleep_menu')
    update.message.reply_text(chosen_msg)
    core_utils.reset_user(context)
    return END

def quit(update, context):
    core_utils.reset_user(context)
    core_utils.ch_menu(context, 'start_menu')
    update.message.reply_text(quit_msg)
    return QUIT

def timeout(update, context):
    core_utils.reset_user(context)
    core_utils.ch_menu(context, 'sleep_menu')
    update.message.reply_text(timeout_msg)
    return END

def no(update, context):
    return NO

def yes(update, context):
    return YES

def invalid(update, context):
    update.message.reply_text('INVALID INPUT')
    return INVALID

def help(update, context):
    dbi = context.bot_data['dbi']
    user_id = update.message.from_user.id
    menu = core_utils.curr_menu(context)
    menu_str = core_utils.generate_menu(menu, dbi, user_id)
    update.message.reply_text(menu_str)
    return 0

# ***** FOR CREATING THREADS *****
def new_thread(update, context):
    
    context.user_data['temp']['new_thread'] = True
    update.message.reply_text(t_title_msg)
    return TITLE

def t_title(update, context):
    # collect previous data
    reply = update.message.text
    context.user_data['temp']['title'] = reply
    # write choices
    dbi = context.bot_data['dbi']
    msg, cats = core_utils.prepare_cats_msg(t_cat_msg, dbi)
    context.user_data['temp']['cats'] = cats
    update.message.reply_text(msg)
    return CAT

def t_cat(update, context):
    reply = update.message.text
    dbi = context.bot_data['dbi']
    cats = context.user_data['temp']['cats']
    print('here')
    try:
        choice = core_utils.cat_choice(reply, cats)
    except:
        print('error found')
        update.message.reply_text(out_of_range_error)
        msg, _ = core_utils.prepare_cats_msg(t_cat_msg, dbi)
        update.message.reply_text(msg)
        return CAT

    context.user_data['temp']['cat'] = choice
    update.message.reply_text(t_body_msg)
    return BODY

def t_body(update, context):
    reply = update.message.text
    context.user_data['temp']['body'] = reply
    update.message.reply_text(t_file_msg)
    return FILE

def t_file(update, context):
    context.user_data['temp']['file_id'], context.user_data['temp']['file_type'] = \
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
    print(context.user_data['temp'])
    msg = core_utils.post_thread(update, context, content, chat_id)
    print(msg)
    author_id = dbi.u_id(author_id) # gets the u_id
    core_utils.log_thread(dbi, thread_id, context, msg, author_id)
    print(str(msg))
    core_utils.reset_user(context)
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
    context.user_data['temp']['tc'] = tc
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
    tc = context.user_data['temp']['tc']
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
    context.user_data['temp']['title'] = reply
    update.message.reply_text(fb_details_msg)
    return BODY

def fb_body(update, context):
    reply = update.message.text
    context.user_data['temp']['body'] = reply
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

###########
# backend #
###########

def all_members(update, context):
    print('TRYING ALL MEMBERS')
    dbi = context.bot_data['dbi']
    users = dbi.get_all_users()
    print(users)
    msg = core_utils.generate_options(users, user_view_msg)
    print('Message,', msg)
    update.message.reply_text(msg)
    return MENU

def ch_perm(update, context):
    dbi = context.bot_data['dbi']
    # gets id, username, user_id, permissions.name
    args = context.args
    user, perms = args[0], args[1]
    print('B4')
    user = core_utils.closest_user(user, dbi)
    print('User', user)
    if not user:
        update.message.reply_text(user_ne_error)
        return MENU
    perms = core_utils.closest_perms(perms, dbi)
    print('Perms', perms)
    if not perms:
        update.message.reply_text(perms_ne_error)
        return MENU
    sender_id = update.message.from_user.id
    # checks if the user that sent this requests is more powerful than reagent
    user_allow = core_utils.compare_perms(sender_id, user, True)
    # checks if the user that sent this requests is more powerful than the perms he is giving
    perms_allow = core_utils.compare_perms(sender_id, perms, True)
    if user_allow and perms_allow:
        old_perm, _ = dbi.get_user_perms(user)
        dbi.ch_perms(perms, user)
        msg = ch_perm_msg.format()
        update.message.reply_text(permi)
    else:
        update.message.reply_text(permission_fail)

    return MENU

# def sel_user(update, context):
#     dbi = context.bot_data['dbi']
#     try:
#         choice = int(context.args[0])
#     except ValueError:
#         update.message.reply_text(not_integer_error)
#         return USER
#     user_ids = context.user_data['temp']['users'].keys()
#     # check if choice is within the possible range
#     if choice in user_ids:
#         context.user_data['temp']['choice_uid'] = choice
#         # gets id, name
#         perms = dbi.get_all_perms()
#         context.user_data['temp']['perms'] = \
#             dict(map(lambda x: [x[0], x[1:]], perms))
#         msg = core_utils.generate_options(perms, sel_perm_msg)
#         update.message.reply_text(msg)
#         return PERMS
#     # goes back to get u_id again
#     else:
#         update.message.reply_text(out_of_range_error)
#         users = context.bot_data['temp']['users']
#         msg = core_utils.generate_options(users, sel_user_msg)
#         update.message.reply_text(msg)
#         return USER


# def sel_perm(update, context):
#     dbi = context.bot_data['dbi']
#     try:
#         choice = int(context.args[0])
#     except ValueError:
#         update.message.reply_text(invalid_input_error)
#         return PERMS
#     perm_ids = context.user_data['temp']['perms'].keys()
#     # check if choice is within range
#     if choice in perm_ids:
#         new_perm = dbi.get_perm(choice)
#         choice_uid = context.bot_data['temp']['choice_uid']
#         username = context.bot_data['temp']['users'][choice_uid][0]
#         old_perm = context.bot_data['temp']['users'][choice_uid][2]
#         update.message.reply_text(ch_perm_msg.format(username, \
#             old_perm, new_perm))
#         # Todo make it say smth
#         return COMPLETED
#     # goes back to get u_id again
#     else:
#         update.message.reply_text(out_of_range_error)
#         perms = context.bot_data['temp']['perms']
#         msg = core_utils.generate_options(perms, sel_perm_msg)
#         update.reply_text(msg)
#         return PERMS


def start(update, context):
    user = update.message.from_user
    user_id = user.id
    dbi = context.bot_data['dbi']
    if dbi.user_exist(user_id):
        update.message.reply_text(text=start_msg)
    else:
        username = user.username
        core_utils.initiate_user(dbi, user)
        update.message.reply_text(text=first_start_msg.format(username))
    return MENU

