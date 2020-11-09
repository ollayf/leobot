import mysql.connector
import utils.db_utils as db_utils

import configparser
config = configparser.ConfigParser()
config.read('bot.cfg')

bot_config = dict(config['test_bot'])
dbi = db_utils.Database(config, 'test_db')
res = dbi.menu_fns('start_menu', 678686611)
print(res)