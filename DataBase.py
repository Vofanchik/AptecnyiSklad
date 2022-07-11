import sqlite3

class DataBase:
    def __init__(self):
        self.conn = sqlite3.connect('sclad.db')
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute(
            '''CREATE TABLE IF NOT EXISTS items_name(
           id integer primary key,
           name text NOT NULL UNIQUE, 
            UNIQUE ("name") ON CONFLICT IGNORE)''')
        self.conn.commit()

    def add_items(self, item_name):
        self.cur.execute("INSERT INTO items_name(name) VALUES(?)", (item_name,))
        self.conn.commit()

    def show_data(self):
        return self.cur.execute('''SELECT name FROM items_name ORDER BY id DESC''').fetchmany(1000)


