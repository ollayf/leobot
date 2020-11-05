import mysql.connector 
import datetime

def dbfmt(name):
    if name is None:
        return 'NULL'

    elif isinstance(name, str):
        return f"'{name}'"
    elif isinstance(name, (int, float)):
        return name
    elif isinstance(name, datetime.datetime):
        name = name.strftime('%Y-%m-%d %H:%M:%S')
        name = f"'{name}'"
        return name
    elif isinstance(name, bool):
        if name:
            return 1
        else:
            return 0
    else:
        rep = repr(name)
        return f'"{rep}"'

class Database():

    def __init__(self, config, section):
        self._setup_db_config(config, section)
        print(str(self.db_config))
        self._connect_DB(self.db_config)

    def _setup_db_config(self, cfg, section):
        '''
        Sets up the config file for leobot
        '''
        section = cfg[section]
        self.db_config = dict(section)
        self.db_config['raise_on_warnings'] = \
            section.getboolean('raise_on_warnings')

    def _connect_DB(self, config):
        '''
        Handles the intial connecting to db
        '''
        db_name = config
        self.cnx = mysql.connector.connect(**config)

        if self.cnx.is_connected():
            print('Connection started')
        else:
            print('Connection failed... Closing app')
            exit()
        self.db = self.cnx.cursor()

    def get_user_perms(self, user_id):
        query = f"""
        SELECT permissions.name, permissions.power
        FROM users 
        LEFT JOIN permissions
        ON users.permissions_id = permissions.id
        WHERE users.user_id = {user_id}
        """
        print(query)
        self.db.execute(query)
        res = self.db.fetchone()
        print('RES:', res)
        return res
    
    def get_fn_perms(self, fn):
        fn = dbfmt(fn)
        query = f"""
        SELECT permissions.name, permissions.id
        FROM functions 
        LEFT JOIN permissions
        ON functions.permissions_id = permissions.id
        WHERE functions.name = {fn}
        """
        print(query)
        self.db.execute(query)
        res = self.db.fetchone()
        print('RES:', res)
        return res

    def new_permissions(self, level, power):
        power = int(power)
        # TODO CONFIRM WITH THE USER IF A SIMILAR PERMISSION EXISTS
        query = f"""
        INSERT INTO permissions (level, power)
        VALUES ('{level}', {power})
        """
        self.db.execute(query)

    def new_user(self, user_id, username, firstname, lastname, permissions_id=7):
        user_id = int(user_id)
        firstname, lastname = dbfmt(firstname), dbfmt(lastname)

        assert isinstance(permissions_id, int), 'permissions id must be int!'
        query = f"""
        INSERT INTO users (user_id, permissions_id, 
        username, firstname, lastname)
        VALUES ({user_id}, {permissions_id}, 
        '{username}', {firstname}, {lastname})
        """ 
        print(query)
        self.db.execute(query)
        self.cnx.commit()

    def user_exist(self, user_id):
        query = f"""
        SELECT username FROM users
        WHERE user_id = {user_id}
        """
        print(query)
        self.db.execute(query)
        res = self.db.fetchone()
        print('res', res)
        if res:
            return res[0]
        else:
            return False

    # for /new_thread
    def get_thread_id(self):
        query = """
        INSERT INTO threads() VALUES ()
        """
        self.db.execute(query)
        self.cnx.commit()
        return self.db.lastrowid

    def new_thread(self, thread_id, msg_id, category_id, msg, title,\
        author_id, post_time, file_id, likes=0, parent_id=None):
        msg_id = int(msg_id)
        parent_id = dbfmt(parent_id)
        author_id = int(author_id)
        category_id = int(category_id)
        likes = int(likes)

        # To handle the ones with text or varchar
        msg = dbfmt(msg)
        file_id = dbfmt(file_id)
        title = dbfmt(title)
        post_time = dbfmt(post_time)
        
        query = f"""
        UPDATE threads SET 
            msg_id = {msg_id},
            parent_id = {parent_id},
            category_id = {category_id},
            msg = {msg},
            likes = {likes},
            post_dt = {post_time},
            title = {title},
            author_id = {author_id},
            file_id = {file_id}
        WHERE id = {thread_id}
        """
        print(query)
        self.db.execute(query)
        self.cnx.commit()
    
    def new_fb(self, author_id, title, msg, file_id, file_type):
        title = dbfmt(title)
        msg = dbfmt(msg)
        file_id = dbfmt(file_id)
        file_type = dbfmt(file_type)
        query = f"""
        INSERT INTO feedback (author_id, title, msg, file_id, file_type)
        VALUES (
            {author_id},
            {title},
            {msg},
            {file_id},
            {file_type}
        )
        """
        self.db.execute(query)
        self.cnx.commit()
    
    def sumview_fb(self):
        query= """
        SELECT id, title
        FROM feedback
        WHERE resolved_dt IS NULL
        """
        self.db.execute(query)
        res = self.db.fetchall()
        return res
    
    def detview_fb(self, id):
        query= f"""
        SELECT title, msg, file_id, file_type
        FROM feedback
        WHERE id = {id}
        """
        print(query)
        self.db.execute(query)
        res = self.db.fetchone()
        return res
    
    def all_issue_ids(self, resolved=None):
        if resolved:
            query = """
            SELECT id FROM feedback
            WHERE resolved_dt IS NOT NULL
            """
        elif resolved == None:
            query = """
            SELECT id FROM feedback
            """
        elif resolved == False:
            query = """
            SELECT id FROM feedback
            WHERE resolved_dt IS NULL
            """
        self.db.execute(query)
        res = self.db.fetchall()
        return res

    def u_id(self, user_id: int):
        query = f"""
        SELECT id FROM users
        WHERE user_id = {user_id}
        """
        self.db.execute(query)
        return self.db.fetchone()[0]

    def cat_id(self, cat: str, tag=False):
        '''
        Returns the category_id of the category given
        '''
        tag = 1 if tag else 0
        cat = dbfmt(cat)
        query = f"""
        SELECT id 
        FROM categories 
        WHERE name = {cat}
        AND tag = {tag};
        """
        print('CAT ID:', query)
        self.db.execute(query)
        res = self.db.fetchone()[0]
        return res
    
    def get_cats(self, tag=False):
        tag = dbfmt(tag)
        query = f"""
        SELECT name, description 
        FROM categories
        WHERE tag = {tag}
        """
        self.db.execute(query)
        res = self.db.fetchall()
        return res
    
    def new_category(self, name: str, tag=0, des=None, parent_id=None):
        name = dbfmt(name)
        des = dbfmt(des)
        tag = 1 if tag else 0
        parent_id = dbfmt(parent_id)
        query = f"""
        INSERT INTO categories (name, description, parent_id, tag)
        VALUES (
            {name},
            {des},
            {parent_id},
            {tag}
        )
        """
        self.db.execute(query)
        self.cnx.commit()

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
        INSERT INTO permissions (name, power) 
	    VALUES
		('members', 0),
		('admin', 10),
		('devs', 100);
        """
        self.db.execute(query)
        # users 
        query = """
        INSERT INTO users (user_id, permissions_id, 
        username, firstname)
        VALUES ( 333647246, 6, 
        'ollayf', 'Hosea')
        """
        self.db.execute(query)
        self.cnx.commit()
