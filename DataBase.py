import sqlite3


class DataBase:
    def __init__(self):
        self.conn = sqlite3.connect('sclad.db')
        self.cur = self.conn.cursor()
        # self.cur.execute('''DROP TABLE quantity''')
        self.create_table()

    def create_table(self):
        self.cur.execute(
            '''CREATE TABLE IF NOT EXISTS items_name(
           id integer primary key,
           name text NOT NULL UNIQUE, 
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

    def add_items(self, item_name):
        self.cur.execute("INSERT INTO items_name(name) VALUES(?)", (item_name,))
        self.conn.commit()

    def add_quantity(self, id_item, quant, quant_sign, date, doc):
        if quant_sign == False:
            quant *= -1
        self.cur.execute("INSERT INTO quantity(item_id, quantity,date_of_insert,doc) VALUES(?,?,?,?)",
                         (id_item, quant, date, doc,))
        self.conn.commit()

    def show_data(self):
        return self.cur.execute('''SELECT name FROM items_name ORDER BY id DESC''').fetchmany(1000)

    def delete_quantity(self, quant_id):
        self.cur.execute(f"DELETE from quantity where id = {quant_id}")
        self.conn.commit()

    def delete_item(self, item_id):
        self.cur.execute(f"DELETE from items_name where id = {item_id}")
        self.cur.execute(f"DELETE from quantity where item_id = {item_id}")
        self.conn.commit()

    def calculate_items(self, item_id):
        return self.cur.execute(f'''SELECT sum(quantity) FROM quantity WHERE item_id = {item_id}''').fetchone()[0]



t = DataBase()
# t.create_table()
# t.add_quantity(1,12,'2020-05-20', 'ТН-2016')
# t.add_quantity(1,12,'2020-05-20', 'ТН-2016')
# t.add_quantity(1,12,'2020-05-20', 'ТН-2016')
# t.add_quantity(2,12,'2020-05-20', 'ТН-2016')
# t.add_quantity(2,500, True, '2020-05-20', 'ТН-2016')
print(t.calculate_items(3))
# t.delete_quantity(1)
# t.delete_item(2)
