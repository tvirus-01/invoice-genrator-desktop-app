import sqlite3, os
from login import check_password_hash

class Database:

    def __init__(self, db):
        self.conn = sqlite3.connect(db, check_same_thread=False)
        self.cur = self.conn.cursor()
        
        sql_create_user_data = """
            CREATE TABLE IF NOT EXISTS 
            user_data (
                id INTEGER PRIMARY KEY, 
                user_name text, 
                gbp_rate text, 
                smtp_server text,
                smtp_user text,
                smtp_sender text,
                smtp_pass text,
                smtp_port text
            )"""
        self.cur.execute(sql_create_user_data)
        self.conn.commit()
        
        sql_create_users = """
            CREATE TABLE IF NOT EXISTS 
            users (
                id INTEGER PRIMARY KEY, 
                user_name text,
                pc_user_name text, 
                password text, 
                user_type text
            )"""
        self.cur.execute(sql_create_users)
        self.conn.commit()

        sql_create_users_session = """
            CREATE TABLE IF NOT EXISTS 
            users_session (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                session_start datetime, 
                session_end datetime
            )"""
        self.cur.execute(sql_create_users_session)
        self.conn.commit()
        
        sql_create_email_condition = """
            CREATE TABLE IF NOT EXISTS 
            email_condition (
                id INTEGER PRIMARY KEY,
                contact_name text, 
                type text
            )"""
        self.cur.execute(sql_create_email_condition)
        self.conn.commit()
        
        sql_create_master_data = """
            CREATE TABLE IF NOT EXISTS 
            master_data (
                id INTEGER PRIMARY KEY, 
                contact_name text, 
                customer_address text, 
                email_id text,
                cc_email_id text,
                description text,
                vat_type text,
                status text
            )"""
        self.cur.execute(sql_create_master_data)
        self.conn.commit()

    def insert_user_data(self, gbp_rate, smtp_server, smtp_port, smtp_user, smtp_sender, smtp_pass):
        user_name = 'admin'

        sql_chk_user = f"SELECT * FROM user_data WHERE user_name = '{user_name}' "
        self.cur.execute(sql_chk_user)
        rows = self.cur.fetchall()

        if len(rows) > 0:
            sql = f"""
                UPDATE user_data SET
                    gbp_rate = '{gbp_rate}',
                    smtp_server = '{smtp_server}',
                    smtp_port = '{smtp_port}',
                    smtp_user = '{smtp_user}',
                    smtp_sender = '{smtp_sender}',
                    smtp_pass = '{smtp_pass}'
                WHERE user_name = '{user_name}'
            """
        else:
            sql = f"""
                INSERT INTO user_data VALUES(
                    NULL,
                    '{user_name}',
                    '{gbp_rate}',
                    '{smtp_server}',
                    '{smtp_user}',
                    '{smtp_sender}',
                    '{smtp_pass}',
                    '{smtp_port}'
                )        
            """
        
        self.cur.execute(sql)
        self.conn.commit()

    def add_master_data(self, contact_name, data):
        contact_name = contact_name.replace("'", "''")
        sql_chk_contact = f"SELECT * FROM master_data WHERE contact_name = '{contact_name}' "
        self.cur.execute(sql_chk_contact)
        rows = self.cur.fetchall()

        if len(rows) > 0:
            pass
        else:
            sql = f"""
                INSERT INTO master_data VALUES(
                    NULL,
                    '{contact_name}',
                    '{data["Customer Address"]}',
                    '{data["Email id"]}',
                    '{data["CC email id"]}',
                    '{data["*Description"]}',
                    '{data["VAT Type"]}',
                    '{data["Status"]}'
                )        
            """
            self.cur.execute(sql)
            self.conn.commit()

    def add_email_condition(self, contact_name, type):
        contact_name = contact_name.replace("'", "''")

        sql_check = f"SELECT * from email_condition WHERE contact_name = '{contact_name}' "
        self.cur.execute(sql_check)
        rows = self.cur.fetchall()

        if len(rows) > 0:
            pass
        else:
            sql = f"""
                INSERT INTO email_condition VALUES(
                    NULL,
                    '{contact_name}',
                    '{type}'
                )        
            """
            self.cur.execute(sql)
            self.conn.commit()

    def fetch_master_data(self, contact_name):
        self.cur.execute(f"SELECT * FROM master_data WHERE contact_name = '{contact_name}' ")
        rows = self.cur.fetchall()
        return rows

    def fetch_user_data(self):
        self.cur.execute(f"SELECT * FROM user_data WHERE user_name = 'admin' ")
        rows = self.cur.fetchall()
        return rows 

    def is_any_user_exists(self):
        self.cur.execute("SELECT * FROM users")
        users = self.cur.fetchall()

        if len(users) > 0:
            return True
        else:
            return False

    def create_user(self, user_name, password, user_type):
        pc_user_name = os.getlogin()

        self.cur.execute(f"SELECT * FROM users WHERE user_name = '{user_name}'")

        if len(self.cur.fetchall()) > 0:
            return "user_name_exists"

        sql = f"INSERT INTO users VALUES(NULL, '{user_name}', '{pc_user_name}', '{password}', '{user_type}' )"
        self.cur.execute(sql)
        self.conn.commit()

    def check_user_login(self, user_name, password, user_type):
        pc_user_name = os.getlogin()

        sql = f"SELECT * FROM users WHERE user_name = '{user_name}' AND pc_user_name = '{pc_user_name}' AND user_type = '{user_type}'"
        self.cur.execute(sql)

        user = self.cur.fetchall()

        if len(user) == 0:
            return "user_not_found"

        user = user[0]
        if not check_password_hash(password, user[3]):
            return "password_err"
        else:
            sql = f"INSERT INTO users_session (id, user_id, session_start) VALUES(NULL, {user[0]}, CURRENT_TIMESTAMP )"
            self.cur.execute(sql)
            self.conn.commit()

            return "login_success"

    def check_user_session(self):
        pc_user_name = os.getlogin()

        sql = f"SELECT * from users u INNER JOIN users_session us ON u.id = us.user_id WHERE u.pc_user_name = '{pc_user_name}' AND us.session_end IS NULL ;"
        self.cur.execute(sql)

        user = self.cur.fetchall()

        if len(user) == 0:
            return "no_session"
        else:
            return user[0]

    def end_user_session(self, session_id):
        self.cur.execute(f"UPDATE users_session SET session_end = CURRENT_TIMESTAMP WHERE id = {session_id}")
        self.conn.commit()

    def fetch_users(self):
        self.cur.execute("SELECT * FROM users WHERE user_type='user' ")
        return self.cur.fetchall()