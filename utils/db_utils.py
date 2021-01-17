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
            print('Connected to {}'.format(config['database']))
        else:
            print('Connection failed... Closing app')
            exit()
        self.db = self.cnx.cursor()
    
    def execute(self, query: str):
        '''
        A wrapper function around the original execute function to check if
        connection is still open. If not start a new connection
        '''
        if not self.cnx.is_connected():
            self._connect_DB(self.db_config)

        self.db.execute(query)

    def get_user_perms(self, user_id):
        if user_id > 10000: # if is a telegram user_id
            query = f"""
            SELECT permissions.name, permissions.power
            FROM users 
            LEFT JOIN permissions
            ON users.permissions_id = permissions.id
            WHERE users.user_id = {user_id}
            """
        else: # if it is just an id in the db
            query = f"""
            SELECT permissions.name, permissions.power
            FROM users 
            LEFT JOIN permissions
            ON users.permissions_id = permissions.id
            WHERE users.id = {user_id}
            """
        self.execute(query)
        res = self.db.fetchone()
        return res
    
    def username2uid(self, username):
        username = dbfmt(username)
        query = f"""
        SELECT id
        FROM users
        WHERE username = {username}
        """
        self.execute(query)
        res = self.db.fetchone()[0]
        return res
    
    def get_all_users(self):
        query="""
        SELECT users.id, users.username, users.user_id, permissions.name
        FROM users
        LEFT JOIN permissions
        ON users.permissions_id = permissions.id
        """
        self.execute(query)
        res = self.db.fetchall()
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
        self.execute(query)
        res = self.db.fetchone()
        return res
    
    def perm_name2id(self, perm):
        perm = dbfmt(perm)
        query=f"""
        SELECT id 
        FROM permissions
        WHERE name = {perm}
        """
        self.execute(query)
        res = self.db.fetchone()[0]
        return res

    def get_all_perms(self):
        query="""
        SELECT id, name 
        FROM permissions
        """
        self.execute(query)
        res = self.db.fetchall()
        return res
    
    def ch_perms(self, new_perm_id, u_id):
        query = f"""
        UPDATE users
        SET permissions_id = {new_perm_id}
        WHERE id = {u_id}
        """
        self.execute(query)
        self.cnx.commit()

    def uid2perms_uname(self, u_id):
        '''
        Mainly created for ch_perms function to get the users username 
        and permissions name
        '''
        query = f"""
        SELECT users.username, permissions.name
        FROM users 
        LEFT JOIN permissions
        ON users.permissions_id = permissions.id
        WHERE users.id = {u_id}
        """
        self.execute(query)
        res = self.db.fetchone()
        return res

    def get_perm(self, perms_id):
        query = f"""
        SELECT name 
        FROM permissions 
        WHERE id = {perms_id}
        """
        self.execute(query)
        res = self.db.fetchone()
        return res

    def perm_dets(self, perms_id):
        query = f"""
        SELECT name, power
        FROM permissions 
        WHERE id = {perms_id}
        """
        self.execute(query)
        res = self.db.fetchone()
        return res

    def menu_fns(self, menu, user_id):
        perm_name, perm_power = self.get_user_perms(user_id)
        perm_name = dbfmt(perm_name)
        query = f"""
        SELECT functions.name, functions.description
        FROM functions
        LEFT JOIN permissions
        ON functions.permissions_id = permissions.id
        WHERE
        (functions.{menu} = 1
        OR functions.all_menu = 1)
        AND 
        (permissions.name = {perm_name}
        OR permissions.power < {perm_power})
        """
        self.execute(query)
        res = self.db.fetchall()
        return res

    def new_permissions(self, level, power):
        power = int(power)
        # TODO CONFIRM WITH THE USER IF A SIMILAR PERMISSION EXISTS
        query = f"""
        INSERT INTO permissions (level, power)
        VALUES ('{level}', {power})
        """
        self.execute(query)
    
    def write_fns_table(self, functions:dict):

        query = """
        DELETE FROM functions;
        ALTER TABLE functions AUTO_INCREMENT = 1
        """
        print(query)
        self.execute(query)
        for key in functions.keys():
            print(key)
            value = functions[key]
            self.new_fn(key, *value)


    def new_fn(self, name, desc, sleep_menu, start_menu, admin_menu, backend, 
        all_menu, in_action=0, permissions_id=1):
        name = dbfmt(name)
        desc = dbfmt(desc)
        query = f"""
        INSERT INTO functions (name, description, sleep_menu,
        start_menu, admin_menu, backend, all_menu, in_action, 
        permissions_id) 
        VALUES
        ({name}, {desc}, {sleep_menu}, {start_menu}, {admin_menu}, {backend},
        {all_menu}, {in_action}, {permissions_id});
        """
        print(query)
        self.execute(query)
        self.cnx.commit()


    def new_user(self, user_id, username, firstname, lastname, permissions_id=1):
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
        self.execute(query)
        self.cnx.commit()

    def user_exist(self, user_id):
        query = f"""
        SELECT username FROM users
        WHERE user_id = {user_id}
        """
        print(query)
        self.execute(query)
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
        self.execute(query)
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
        self.execute(query)
        self.cnx.commit()
    
    def del_thread(self, id):
        # first gets the msg_id of the thread
        query = f"""
        SELECT msg_id
        FROM threads
        WHERE id = {id}
        """
        self.execute(query)
        msg_id = self.db.fetchone()[0]
        # deletes the row from the table
        query = f"""
        UPDATE threads
        SET deleted = 1
        WHERE id = {id}
        """
        print('msg id', msg_id)
        print(query)
        self.execute(query)
        self.cnx.commit()
        return msg_id


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
        self.execute(query)
        self.cnx.commit()
    
    def sumview_fb(self):
        query= """
        SELECT id, title
        FROM feedback
        WHERE resolved_dt IS NULL
        """
        self.execute(query)
        res = self.db.fetchall()
        return res
    
    def detview_fb(self, id):
        query= f"""
        SELECT title, msg, file_id, file_type
        FROM feedback
        WHERE id = {id}
        """
        print(query)
        self.execute(query)
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
        self.execute(query)
        res = self.db.fetchall()
        return res

    def u_id(self, user_id: int):
        query = f"""
        SELECT id FROM users
        WHERE user_id = {user_id}
        """
        self.execute(query)
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
        self.execute(query)
        res = self.db.fetchone()[0]
        return res
    
    def get_cats(self, tag=False):
        tag = dbfmt(tag)
        query = f"""
        SELECT name, description 
        FROM categories
        WHERE tag = {tag}
        """
        self.execute(query)
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
        self.execute(query)
        self.cnx.commit()

    def close(self):
        self.cnx.close()

    def resetDB(self):
        '''
        Don't use unless you know what you are doing
        '''
        self.execute("""SHOW TABLES""")

        tables = self.db.fetchall()
        for table in tables:
            query = f"""DELETE FROM {table[0]};"""
            print(query)
            self.execute(query)
        
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
        self.execute(query)
        # users 
        query = """
        INSERT INTO users (user_id, permissions_id, 
        username, firstname)
        VALUES ( 333647246, 6, 
        'ollayf', 'Hosea')
        """
        self.execute(query)
        self.cnx.commit()
