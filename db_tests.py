import mysql.connector
import utils.db_utils as db_utils

import configparser
config = configparser.ConfigParser()
config.read('bot.cfg')

bot_config = dict(config['test_bot'])
print(str(config))
dbi = db_utils.Database(config, 'test_db')
dbi.init_db()