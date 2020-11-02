import utils.logic as logic
from telegram.ext import Filters, MessageHandler
import logging
from collections import defaultdict
import telegram
import time
from functools import wraps
from leo_msgs import *

####################
# INITIALISING BOT #
####################

#########
# USERS #
#########

def setup_bot_data(dp, owner, bot_cfg, dbi, testing):
    chat_id = bot_cfg['chat_id']
    bot_data = {
        'owner': owner,
        'dbi': dbi,
        'bot_cfg': bot_cfg,
        'chat_id': chat_id
    }
    dp.bot_data = bot_data


def initiate_user(dbi, user):
    user_id = user.id
    username = user.username
    firstname = user.first_name
    lastname = user.last_name
    if firstname is None:
        firstname = username
    dbi.new_user(user_id, username, firstname, lastname)

def menu_activated(user_data):
    '''
    Checks if any menu is currently activated
    Returns True if it is and False if it isn't
    '''
    menus = ['admin_menu', 'backend', 'confirmation', 'birthday']
    status_dict = user_data['status']
    result = False
    # checks if any of the menus are accessed currently
    for menu in menus:
        # if this condition is never invoked, result will return False
        if status_dict[menu]:
            result = True
    
def check_permissions(fn, user_id, dbi):
    print('getting usert perms')
    user_l, user_p = dbi.get_user_perms(user_id)
    print('getting fn perms')
    fn_l, fn_p = dbi.get_fn_perms(fn)
    # no requirement for this command
    if not (fn_l or fn_p):
        return True
    elif fn_l == user_l or user_p > fn_p:
        return True
    else:
        return False

def set_user_data_to_default(update, context, default_user_data):
    '''
    Recursively sets user_data of this user to default user_data
    '''
    assert isinstance(default_user_data, (dict, defaultdict)), \
        'default user data must be a defaultdict or dict'
    # recursively add the attributes of the dictionary
    for key in default_user_data.keys():
        # make the list or dictionary immutable
        if isinstance(default_user_data[key], (dict, list)):
            context.user_data[key] = default_user_data[key].copy()
        else:
            context.user_data[key] = default_user_data[key]

def close_all_menus(user_data):
    '''
    Closes all menus in the conversation
    If a new menu is added, change this function and the next only
    '''
    user_data['status']['admin_menu'] = False
    user_data['status']['backend'] = False
    user_data['status']['cfm_settings'] = False
    user_data['status']['bday_settings'] = False

def clear_user_memory(user_data, end=False, quit=False):
    '''
    in an event such as ending the bot, reset all the attributes of the user to default
    '''
    pass

###########
# general #
###########

def get_msg_file(message: telegram.Message):
    file_id, file_type = None, None
    file = message.photo or message.video or message.audio or \
           message.voice or message.document
    print(file)
    if isinstance(file, list):
        file = file[-1]
    elif isinstance(file, dict):
        pass
    if file is None:
        pass
    else:
        file_id, file_type = file.file_id, type(file)

    return file_id, file_type

###########
# THREADS #
###########

class TagChecker():
    confirmed = False
    curr_id = 0

    def __init__(self, tags: list, ref: list, dbi):
        self.tags = tags
        self.max = len(tags)
        self._process_tags(ref)
        self.dbi = dbi

    def _process_tags(self, ref):
        final_tags = []
        for tag in self.tags:
            res = logic.closest_matches(tag, ref)
            
            # if the are a list of closest matches
            if isinstance(res, list):
                res.append(None)
                closest_dict = dict(enumerate(res, 1))
                final_tags.append(closest_dict)
            # if there is a clear result
            else:
                final_tags.append(res)
        # set the final_tags
        self.final_tags = final_tags

    def next(self):
        while self.curr_id < self.max:
            self.curr_tag = self.final_tags[self.curr_id]
            self.curr_id += 1
            if isinstance(self.curr_tag, dict):
                return self.curr_tag
        return None
    
    def update_curr(self, choice: int):
        print('current tag', self.curr_tag)
        ans = self.curr_tag[choice]
        # creates a new tag if users wishes
        if ans is None:
            ans = self.tags[self.curr_id-1]
            print(ans)
            self.dbi.new_category(ans, 1)
        # replaces the list with the chosen result
        self.final_tags[self.curr_id-1] = ans
        print('final tgas', self.final_tags)

    def prepare_tc_qn(self, template):
        tag_input = self.tags[self.curr_id-1]
        template = template.format(tag_input)
        choices = self.curr_tag
        for key in choices.keys():
            value = choices[key]
            if value is None:
                line = 'None of the above, create new tag'
            else:
                line = value
            line = f'\n{key}: {line}'
            template += line
        return template

def prepare_cats_msg(msg, dbi):
    cats = dbi.get_cats()
    cats = dict(enumerate(cats, 1))
    for key in tuple(cats.keys()):
        msg += f'\n{key}: {cats[key][0]} -- {cats[key][1]}'
    return msg, cats

def cat_choice(reply, cats):
    reply = reply.split()[0]
    try:
        choice = int(reply)
    except ValueError:
        return None
    
    cat = cats[choice][0]
    return cat

def parse_tags(msg):
    tags = msg.split(',')
    tags = list(map(lambda x: x.split(), tags))
    final_tags = []
    for tag in tags:
        if isinstance(tag, list):
            tag = list(map(lambda x: x.capitalize(), tag))
            new_tag = '_'.join(tag)
            final_tags.append(new_tag)
        elif isinstance(tag, str):
            tag = tag.capitalize()
            final_tags.append(tag)
    
    return final_tags

def get_thread_data(context):

    category = context.user_data['cat']
    title = context.user_data['title']
    body = context.user_data['body']
    tags = context.user_data['tc'].final_tags
    return category, title, body, tags

def prepare_tags(tags: list):
    tags = list(map(lambda x: f'\#{x}', tags))
    tags = ', '.join(tags)
    return tags

def prepare_thread(context, template, thread_id):
    category, title, body, tags = get_thread_data(context)
    tags = prepare_tags(tags)
    content = template.format(thread_id=thread_id, category=category, \
                                title=title, body=body, tags=tags)
    print('content,', content)
    return content

def post_thread(update, context, content, chat_id):
    user_data = context.user_data
    bot = context.bot
    fns = {
        telegram.PhotoSize: bot.send_photo,
        telegram.Video: bot.send_video,
        telegram.Audio: bot.send_audio,
        telegram.Voice: bot.send_voice,
        telegram.Document: bot.send_document,
        None: bot.send_message
    }
    fn = fns[user_data['file_type']]
    if fn == bot.send_message:
        msg = fn(chat_id, content, parse_mode='MarkdownV2')
    else:
        msg = fn(chat_id, user_data['file_id'], caption=content,\
             parse_mode='MarkdownV2')
    
    return msg

def log_thread(dbi, thread_id, context, msg, author_id):
    """
    Logs the posted thread into the db
    """
    category, title, body, tags = get_thread_data(context)
    print('MESSAGE TYPE', type(msg))
    msg_id = msg.message_id
    post_time = msg.date
    cat_id = dbi.cat_id(category)
    file_id = context.user_data['file_id']
    print(type(post_time), post_time)
    dbi.new_thread(thread_id, msg_id, cat_id, body, title, author_id,
        post_time, file_id)
    print('Logged thread')
    
############
# feedback #
############
def get_fb_details(context):
    user_data = context.user_data
    title = user_data['title']
    body = user_data['body']
    return title, body

def sumview_fb(dbi):
    final_content = []
    issues = dbi.sumview_fb()
    print('ISSUES:', issues)
    for id, title in issues:
        line = fb_sumview_temp.format(id = id, title=title)
        final_content.append(line)
    final_content = '\n'.join(final_content)
    return final_content

def detview_fb(id, dbi, update, context):
    msg = update.message
    chat_id = context.bot_data['owner']
    fns = {
        "<class 'telegram.files.photosize.PhotoSize'>": msg.reply_photo,
        "<class 'telegram.files.audio.Audio'>": msg.reply_audio,
        "<class 'telegram.files.voice.Voice'>": msg.reply_voice,
        "<class 'telegram.files.document.Document'>": msg.reply_document,
        "<class 'telegram.files.video.Video'>": msg.reply_video,
        None: msg.reply_text
    }
    res = dbi.detview_fb(id)
    if res is None:
        msg = msg.reply_text(out_of_range_error)
    else:
        print('RES:', res)
        title, body, file_id, file_type = res
        content = fb_detview_temp.format(id=id, title=title, msg=body)
        fn = fns[file_type]
        print('content:', content)
        print('fucntion;', fn)
        if fn == msg.reply_text:
            msg = fn(content)
        else:
            msg = fn(file_id, caption=content,\
                parse_mode='MarkdownV2')
    return msg

##############
# MISC UTILS #
##############
def bot_print(update, text):
    '''
    replies a certain msg to the sender
    '''
    if type(text) != str:
        text = str(text)
    update.message.reply_text(text=text)

def file_handler(fn):
    return MessageHandler(Filters.photo | Filters.document \
            | Filters.video | Filters.audio | \
            Filters.voice & ~Filters.command, fn)

########################
# IMPORTANT DECORATORS #
########################

def send_typing_action(func):
    '''Sends typing action while func command.
    Just: 
    @send_typing_action
    def my_handler(update, context):
        pass
    '''
    
    @wraps(func)
    def typing_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id, \
            action=telegram.ChatAction.TYPING)
        return func(update, context)

    return typing_func

def time_execution(fn):
    '''
    This function is meant to be a decorator to time any function that is happening
    Prints the time taken to complete function in second(s)
    '''
    def timer(*args, **kwargs):
        start = time.time()
        # run the function
        fn(*args, **kwargs)
        end = time.time()
        time_taken = end - start
        print(time_taken)
    return timer

if __name__ == '__main__':
    pass