import mysql.connector 
import datetime

class Database():

    def __init__(self, config, section):
        self._setup_db_config(config, section)
        print(str(self.db_config))
        self._connect_DB(self.db_config)

    def _setup_db_config(self, cfg, section):
        section = cfg[section]
        self.db_config = dict(section)
        self.db_config['raise_on_warnings'] = \
            section.getboolean('raise_on_warnings')

    def _connect_DB(self, config):
        '''
        Handles the intial connecting to db
        '''
        self.cnx = mysql.connector.connect(**config)

        print(self.cnx.is_connected())
        self.db = self.cnx.cursor()

    def new_permissions(self, level, power):
        power = int(power)
        # TODO CONFIRM WITH THE USER IF A SIMILAR PERMISSION EXISTS
        query = f"""
        INSERT INTO permissions (level, power)
        VALUES ('{level}', {power})
        """
        self.db.execute(query)

    def new_category(self, name, desc, tag):
        assert isinstance(tag, bool), 'Tag must be boolean'
        query = f"""
        INSERT INTO categories (name, description, tag)
        VALUES ('{name}', '{desc}', {tag})
        """
        self.db.execute(query)

    def new_user(self, user_id, username, firstname, lastname, permissions_id=4):
        user_id = int(user_id)
        assert isinstance(permissions_id, int), 'permissions id must be int!'
        query = f"""
        INSERT INTO users (user_id, permissions_id, 
        username, firstname, lastname)
        VALUES ({user_id}, {permissions_id}, 
        '{username}', '{firstname}', '{lastname}')
        """
        self.db.execute(query)
        self.cnx.commit()

    def user_exist(self, user_id):
        query = f"""
        SELECT username FROM users
        WHERE user_id = {user_id}
        """
        self.db.execute(query)
        res = self.db.fetchall()
        if res:
            return res[0]
        else:
            return False

    def new_thread(self, msg_id, category_id, msg, title,\
        likes, origin_id, parent_id=None):
        msg_id = int(msg_id)
        if parent_id:
            parent_id = int(parent_id)
        origin_id = int(origin_id)
        category_id = int(category_id)
        like = int(likes)

        post_time = datetime.datetime.now()
        
        query = f"""
        INSERT INTO threads (msg_id, parent_id, category_id, msg, post_time
        title, likes, origin_id)
        VALUES ({msg_id}, {parent_id}, {category_id}, '{msg}', {post_time},
        '{title}', '{likes}', '{origin_id}'
        )
        """
        self.db.execute(query)


    def close(self):
        self.cnx.close()

    def resetDB(self):
        '''
        Don't use unless you know what you are doing
        '''
        self.db.execute("""SHOW TABLES""")

        tables = self.db.fetchall()
        for table in tables:
            query = f"""DELETE FROM {table[0]};"""
            print(query)
            self.db.execute(query)
        
        self.cnx.commit()
    

    def init_db(self):

        # permissions
        query = """
        INSERT INTO permissions (level, power) 
	    VALUES
		('members', 0),
		('admin', 10),
		('devs', 100);
        """
        self.db.execute(query)
        # users 
        query = f"""
        INSERT INTO users (user_id, permissions_id, 
        username, firstname, lastname)
        VALUES ( 333647246, 6, 
        'ollayf', 'Hosea', None)
        """
        self.cnx.commit()


