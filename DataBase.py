import sqlite3
from datetime import date

from XlsxImport import XlsxImport



class DataBase:
    def __init__(self):
        self.conn = sqlite3.connect('sclad.db')
        self.cur = self.conn.cursor()
        # self.cur.execute('''DROP TABLE quantity''')
        # self.cur.execute('''DROP TABLE items_name''')
        self.create_table()

    def create_table(self):
        self.cur.execute(
            '''CREATE TABLE IF NOT EXISTS items_name(
           id integer primary key,
           name text NOT NULL UNIQUE, 
           unit text DEFAULT "уп",
            UNIQUE ("name") ON CONFLICT IGNORE)''')
        self.conn.commit()

        self.cur.execute(
            '''CREATE TABLE IF NOT EXISTS quantity(
           id integer primary key,
           item_id INTEGER,
           quantity REAL NOT NULL,
           date_of_insert TEXT,
           doc TEXT,
           FOREIGN KEY (item_id) REFERENCES items_name(id))
           ''')
        self.conn.commit()

        self.cur.execute(
            '''CREATE TABLE IF NOT EXISTS units(
           id integer primary key,
           name text NOT NULL UNIQUE, 
            UNIQUE ("name") ON CONFLICT IGNORE)''')
        self.conn.commit()



    def add_items(self, item_name, unit):
        self.cur.execute("INSERT INTO items_name(name, unit) VALUES(?,?)", (item_name, unit,))
        self.cur.execute("INSERT INTO units(name) VALUES(?)", (unit,))
        self.conn.commit()
        return self.cur.lastrowid

    def add_quantity(self, id_item, quant, quant_sign, date, doc):
        if quant_sign == False:
            quant *= -1
        self.cur.execute("INSERT INTO quantity(item_id, quantity,date_of_insert,doc) VALUES(?,?,?,?)",
                         (id_item, quant, date, doc,))
        self.conn.commit()

    def show_data(self):
        return self.cur.execute('''SELECT id, name FROM items_name ORDER BY id ASC''').fetchmany(10000)

    def delete_quantity(self, quant_id):
        self.cur.execute(f"DELETE from quantity where id = {quant_id}")
        self.conn.commit()

    def delete_item(self, item_id):
        self.cur.execute(f"DELETE from items_name where id = {item_id}")
        self.cur.execute(f"DELETE from quantity where item_id = {item_id}")
        self.conn.commit()

    def calculate_items(self, item_id):
        return self.cur.execute(f'''SELECT sum(quantity) FROM quantity WHERE item_id = {item_id}''').fetchone()[0]

    def import_from_xls(self, file_name, date_today):
        p = XlsxImport(file_name)
        data = p.import_into_list()
        for i in data:
            b = self.add_items(i[0], i[1])
            info = self.cur.execute('SELECT * FROM items_name WHERE id=?', (b,))
            if info.fetchone() is None:
                return
            else:
                self.add_quantity(b, i[2], True, date_today, '')

t = DataBase()
# t.import_from_xls('wb1.xlsx', date.today())
# t.add_quantity(8, 10, False, date.today(), 'Инфекционное')
# print(t.calculate_items(8))
print(t.show_data())

