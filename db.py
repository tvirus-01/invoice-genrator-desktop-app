import sqlite3, os

class Database:

    def __init__(self, db):
        self.conn = sqlite3.connect(db)
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
        user_name = os.getlogin()

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

    def fetch_master_data(self, contact_name):
        self.cur.execute(f"SELECT * FROM master_data WHERE contact_name = '{contact_name}' ")
        rows = self.cur.fetchall()
        return rows

    def fetch_user_data(self):
        self.cur.execute(f"SELECT * FROM user_data WHERE user_name = '{os.getlogin()}' ")
        rows = self.cur.fetchall()
        return rows 