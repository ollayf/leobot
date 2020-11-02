'''
This script contains all the usual messages such as:
- Error messages
- Intiialising messages
- Successful action messages
'''

########################
# DEFAULT SETUP CONFIG #
########################

# TODO: What is displayed when asked for the info of the bot
BOT_DESCRIPTION = ''

##   MESSAGES
##############

bot_init_msg = 'Energise!'

###########
# threads #
###########
t_title_msg = 'May I have the title of your thread?'
t_cat_msg = 'Which category can this thread be considered under?'
t_body_msg = 'What is the main content or body of your thread?'
t_file_msg = 'Is there any file you would like to include? Currently \
we accept: Audio, Video, Images, Voice Messages, Documents \n\
/no if you do not want to submit a file'
t_tags_msg = 'Are there any tags you would like to include?'
t_tagger_msg = 'There are some tags that are new to our database. \
It is important to ensure consistency in tag names so that people can \
see your posts.'
t_tags_check_msg = 'Which of these tags are closest to what you mean? \
your input: {}'
t_complete_msg = 'Thanks for your submission!'
# no_file_msg = 'Thank you we will post this thread without a file

################
# get feedback #
################
fb_title_msg = 'Please state the issue subject.'
fb_details_msg = 'Please provide more details about this issue. \
You can also leave a simple "-" or "NA"'
fb_file_msg = 'Do you want to upload a file for this issue?\n\
/no if you do not want to submit a file.'
fb_complete_msg = 'Thank you for your feedback. A Moderator will respond to \
you ASAP'
fb_sumview_temp = '**{id}**: __{title}__'
fb_detview_temp = """__{id}: {title}__ 
{msg}"""

################
# Fundamentals #
################
start_msg = """Welcome Sir/Ma'am, What would you like to do today?
/new_thread -- start a thread
/feedback -- give me feedback 
/end -- end the convo with me"""

admin_menu_msg = """Welcome Admin {}! What would you like to do today?

/sview_fb -- Look at a summary of unresolved feedback
/dview_fb <feedback id> -- Look at the details of a specific feedback"""

# when a user initialises the bot for the first time
first_start_msg = """Welcome {}! Is this your first time? Hi my name is leobot. I store important \
information and do particular administrative tasks to aide the running of LG. However just \
like you I am not perfect, so please do not hesitate to give me feedback on how I can serve you \
and the LG better. You can use \n/feedback to give me your feedback

Commands you can use without doing /start (for quick use):
/start -- start a conversation with me :)
/end -- end the conversation
/tutorial -- a simple tutorial to test the functions (will be erased after /end)
/help -- can be used at any time to give the list of possible functions"""

timeout_msg="Sorry sir/ma\'am, this session has automatically been ended. \
Goodbye..."

end_msgs = ['Going so soon.... Alright... Bye then...',\
    'Cheerio',\
    'Have nice day',\
    'Thank you for your time. Goodbye',\
    'k thx bai'
    ]

##################
# ERROR MESSAGES #
##################

# TODO: I USED THIS TO MAKE ENDING THE BOT SLIGHTLY MORE INTERESTING
fail_end_msgs = ['Wait bruh we aren\'t even in a conversation...',\
    'Uhm ok... It\'s not like i wanted to talk to you anyway',\
    'Wait whats there to end? Wait end me?!! Why do you want to end me?!'
    ]

not_started_error = 'Hello... Please start a conversation with me first with /start'
not_integer_error = 'Value is not an integer. Try inputting index again'
out_of_range_error = 'Index out of range'
one_arg_error = 'Only 1 argument allowed to be input'
not_exist_error = 'this person does not exist'
cancel_fail = 'You are not currently in an action!'
permission_fail = 'You have no power here!'
function_fail = 'This function is not allowed in the mode you have activated. E.G. admin_menu'
quit_fail = 'bruh there\'s nothing to quit lol'
user_timeout_msg = '15 minutes is up, I will automatically be going to sleep. Please remember \
to end the conversation when not in use.\nYou can also use /events, /library, /start_call \
/end_call without starting me up.'

######################
# SUCCESSFUL ACTIONS #
######################

cancel_msg = 'Alrighty! Action cancelled!'

# I USED THIS TO MAKE ENDING THE BOT SLIGHTLY MORE INTERESTING (a message is randomly selecting when 
# the user ends the session)

# 
quit_fin_msg = 'Thanks bro. Goodbye!'

# THREAD TEMPLATES
template_1 = """\
__{thread_id}: {title}__
*{category}*

{body}

*{tags}*
"""