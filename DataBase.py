import sqlite3

from XlsxImport import XlsxImport


class DataBase:
    def __init__(self):
        self.id = None
        self.conn = sqlite3.connect('sclad.db')
        self.cur = self.conn.cursor()
        self.create_table()

    def create_group(self, name):  # создаесм переменные таблицы

        self.cur.execute("INSERT INTO groups(name) VALUES(?)", (name,))  # создаём группу товаров
        self.conn.commit()

        self.id = self.cur.lastrowid  # присваиваем id последней созданной группы
        print(self.id)
        self.cur.execute(  # создаем таблицу с названием items_id для каждой группы
            f'''CREATE TABLE IF NOT EXISTS items{self.id}(
           id integer primary key,
           name text NOT NULL UNIQUE,             
           unit text DEFAULT "уп",
            mnn_name text NOT NULL default "",
            UNIQUE ("name") ON CONFLICT IGNORE)''')
        self.conn.commit()

        self.cur.execute(  # таблица quantity будет содержать все операции по приему выдаче
            f'''CREATE TABLE IF NOT EXISTS quantity{self.id}(
           id integer primary key,
           item_id INTEGER,
           quantity REAL NOT NULL,
           date_of_insert TEXT,
           doc TEXT,
           FOREIGN KEY (item_id) REFERENCES items{self.id}(id))
           ''')
        self.conn.commit()

    def delete_group(self, id_gr: int):
        self.cur.execute(f'DELETE from groups where id = {id_gr}')
        self.cur.execute(f'DROP TABLE IF EXISTS quantity{id_gr}')
        self.cur.execute(f'DROP TABLE IF EXISTS items{id_gr}')
        self.conn.commit()

    def create_table(self):  # создаем постоянные таблицы

        self.cur.execute(  # Группы ценностей
            '''CREATE TABLE IF NOT EXISTS groups(
           id integer primary key,
           name text NOT NULL UNIQUE, 
            UNIQUE ("name") ON CONFLICT IGNORE)''')
        self.conn.commit()

        self.cur.execute(  # еденицы измерения
            '''CREATE TABLE IF NOT EXISTS units(            
           id integer primary key,
           name text NOT NULL UNIQUE, 
            UNIQUE ("name") ON CONFLICT IGNORE)''')
        self.conn.commit()

        self.cur.execute(  # отделение
            '''CREATE TABLE IF NOT EXISTS division(
           id integer primary key,
           name text NOT NULL UNIQUE, 
            UNIQUE ("name") ON CONFLICT IGNORE)''')
        self.conn.commit()

        self.cur.execute(  # МНН для препаратов
            '''CREATE TABLE IF NOT EXISTS mnn(
           id integer primary key,
           name text NOT NULL UNIQUE, 
            UNIQUE ("name") ON CONFLICT IGNORE)''')
        self.conn.commit()


    def add_items(self, item_name, unit, mnn=''):  # создаем товар
        self.cur.execute(f"INSERT INTO items{self.id}(name, unit, mnn_name) VALUES(?,?,?)", (item_name, unit, mnn,))
        self.cur.execute("INSERT INTO units(name) VALUES(?)", (unit,))
        self.cur.execute("INSERT INTO mnn(name) VALUES(?)", (mnn,))
        self.conn.commit()
        return self.cur.lastrowid

    def add_quantity(self, id_item, quant, quant_sign, date, doc):  # добавляем приход, расход (с минусом в quant_sign)
        if not quant_sign:
            quant *= -1
            self.cur.execute("INSERT INTO division(name) VALUES(?)", (doc,))

        self.cur.execute(f"INSERT INTO quantity{self.id}(item_id, quantity,date_of_insert,doc) VALUES(?,?,?,?)",
                         (id_item, quant, date, doc,))
        self.conn.commit()

    def show_package(self):  # возвращаем Упаковки
        try:
            return self.cur.execute(f'''SELECT name FROM units''').fetchmany(10000)
        except:
            return []

    def show_mnn(self):  # возвращаем Упаковки
        try:
            return self.cur.execute(f'''SELECT name FROM mnn''').fetchmany(1000000)
        except:
            return []


    def show_data(self):  # возвращаем 10000  записей товара
        try:
            return self.cur.execute(f'''SELECT id, name, unit FROM items{self.id} ORDER BY id ASC''').fetchmany(10000)
        except:
            return []

    def delete_quantity(self, quant_id):  # удаляем проиход/расход
        self.cur.execute(f"DELETE from quantity{self.id} where id = {quant_id}")
        self.conn.commit()

    def delete_item(self, item_id):  # удаляем товар
        self.cur.execute(f"DELETE from items{self.id} where id = {item_id}")
        self.cur.execute(f"DELETE from quantity{self.id} where item_id = {item_id}")
        self.conn.commit()

    def calculate_items(self, item_id):  # возвращаем остаток товара
        return \
            self.cur.execute(f'''SELECT sum(quantity) FROM quantity{self.id} WHERE item_id = {item_id}''').fetchone()[0]

    def import_from_xls(self, file_name, date_today):  # импортируем из экселя
        p = XlsxImport(file_name)
        data = p.import_into_list()
        for i in data:
            b = self.add_items(i[0], i[1])
            info = self.cur.execute(f'SELECT * FROM items{self.id} WHERE id=?', (b,))
            if info.fetchone() is None:
                return
            else:
                self.add_quantity(b, i[2], True, date_today, '')

    def select_quant_by_date(self, from_date, to_date):  # возвращаем проиход/расход товара за период времени
        return self.cur.execute(
            f'''SELECT * FROM quantity{self.id} LEFT JOIN items{self.id} ON quantity{self.id}.item_id = items{self.id}.id
                                    WHERE date_of_insert BETWEEN "{from_date}" AND "{to_date}"''').fetchmany(10000)

    def show_quantyty_by_id_date(self, id_item, from_date, to_date):
        return self.cur.execute(
            f'''SELECT * FROM quantity{self.id} 
                WHERE date_of_insert BETWEEN "{from_date}" AND "{to_date}"
                AND item_id = {id_item}''').fetchmany(10000)

    def return_residue(self):  # считает остатки по всем позициям
        all_residue = []
        for a in self.show_data():
            one_residue = [a[1], a[2], str(self.calculate_items(a[0])).replace('.0 ', '')]
            all_residue.append(one_residue)

        return all_residue

    def show_data_of_groups(self):  # возвращаем 10000  записей товара
        return self.cur.execute(f'''SELECT id, name FROM groups ORDER BY id ASC''').fetchmany(10000)

    def get_id_from_items(self, item_name):
        return self.cur.execute(
            f'''SELECT id FROM items{self.id} 
                        WHERE name = "{item_name}"''').fetchone()


t = DataBase()
# t.delete_group(6)
t.id = 1
# print(t.show_data_of_groups())


# print()
# t.create_group('пенис')
# t.import_from_xls('wb1.xlsx', date.today())
# t.add_quantity(1, 10, False, '2022-06-14', 'Инфекционное')
# t.delete_item(9)
# print(t.calculate_items(1))
# print(t.select_quant_by_date("2022-06-14", "2023-08-31"))
# print(t.show_quantyty_by_id_date(1,"2022-06-14", "2023-08-31"))
