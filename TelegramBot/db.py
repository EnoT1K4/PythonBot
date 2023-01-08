import sqlite3
import time

class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cur = self.connection.cursor()

    def user_exists(self, user_id, ):
        with self.connection:
            result = self.cur.execute("""SELECT * FROM users WHERE user_id = ?""", (user_id,)).fetchall()
            return bool(len(result))

    def add_user(self, user_id, user_name):
        with self.connection:
            return self.connection.execute("""INSERT INTO users ('user_id') ('user_name') VALUES (?,?)""", (user_id, user_name))

    def mute(self, user_id):
        with self.connection:
            user = self.cur.execute("""SELECT * FROM users WHERE user_id = ?""", (user_id,)).fetchone()
            return int(user[2] >= int(time.time()))

    def add_mute(self, user_id, mute_time):
        with self.connection:
            return self.connection.execute("""UPDATE users SET 'mute_time' = ? WHERE 'user_id' = ?""", (int(time.time() + mute_time), user_id,))

    def name(self,user_id):
        with self.connection:
            return self.cur.execute("""SELECT user_name FROM users WHERE (?) = user_id""", (user_id,)).fetchall()

    def add_admin(self, user_id):
        with self.connection:
            return self.connection.execute("""INSERT INTO admins ('id') VALUES (?)""", (user_id,))

    def add_nick(self, user_id, user_name):
        with self.connection:
            self.cur.execute("""DELETE FROM nickname WHERE id = (?)""", (user_id,))
            return self.cur.execute("""INSERT INTO nickname VALUES (?,?)""", (user_name, user_id))

    def change_name(self):
        with self.connection:
            return self.cur.execute("""UPDATE users SET user_name = (SELECT nickname FROM nickname WHERE user_id = id)""")

    def get_admID(self):
        with self.connection:
            return self.cur.execute("""SELECT * FROM admins""").fetchall()

    def get_users(self):
        with self.connection:
            return self.cur.execute("""SELECT user_id, user_name FROM users, nickname WHERE (users.user_id = nickname.id)""").fetchall()

    def add_link(self, user_id, link):
        with self.connection:
            return self.connection.execute(""" INSERT INTO links VALUES (?,?) """, (user_id, link))
    def get_link(self):
        with self.connection:
            return self.cur.execute("""SELECT user_id, link FROM links, users WHERE (links.id = users.user_id)""").fetchall()
