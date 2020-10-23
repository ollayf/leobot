import configparser
env = configparser.ConfigParser()
env.read('./bots.cfg')

print(env['test_db'].getboolean('raise_on_warnings'))