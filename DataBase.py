import sqlite3
from datetime import date
from pprint import pprint

from ODF_import_expor import OdsExport
from XlsxImport import XlsxImport


class DataBase:
    def __init__(self):
        self.id = None
        self.conn = sqlite3.connect('sclad.db')
        self.cur = self.conn.cursor()
        self.create_table()

    def show_item_by_id(self, id_item):
        return self.cur.execute(
            '''SELECT name, unit, mnn_name FROM items{}
             WHERE id = {}'''.format(self.id, id_item)).fetchone()

    def change_item(self, name, package, mnn, id):
        self.cur.execute("UPDATE items{} SET name = '{}', unit = '{}', mnn_name = '{}' WHERE id = '{}'"
                         .format(self.id, name, package, mnn, id))
        self.conn.commit()

    def create_group(self, name):  # создаесм переменные таблицы

        self.cur.execute("INSERT INTO groups(name) VALUES(?)", (name,))  # создаём группу товаров
        self.conn.commit()

        self.id = self.cur.lastrowid  # присваиваем id последней созданной группы
        self.cur.execute(  # создаем таблицу с названием items_id для каждой группы
            '''CREATE TABLE IF NOT EXISTS items{}(
           id integer primary key,
           name text NOT NULL UNIQUE,             
           unit text DEFAULT "уп",
            mnn_name text NOT NULL default "",
            UNIQUE ("name") ON CONFLICT IGNORE)'''.format(self.id))
        self.conn.commit()

        self.cur.execute(  # таблица quantity будет содержать все операции по приему выдаче
            '''CREATE TABLE IF NOT EXISTS quantity{}(
           id integer primary key,
           item_id INTEGER,
           quantity REAL NOT NULL,
           date_of_insert TEXT,
           doc TEXT,
           FOREIGN KEY (item_id) REFERENCES items{}(id))
           '''.format(self.id, self.id))
        self.conn.commit()

    def delete_group(self, id_gr: int):
        self.cur.execute('DELETE from groups where id = {}'.format(id_gr))
        self.cur.execute('DROP TABLE IF EXISTS quantity{}'.format(id_gr))
        self.cur.execute('DROP TABLE IF EXISTS items{}'.format(id_gr))
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

        self.cur.execute("INSERT INTO units(name) VALUES(?)", (unit,))
        self.cur.execute("INSERT INTO mnn(name) VALUES(?)", (mnn,))
        self.cur.execute("INSERT INTO items{}(name, unit, mnn_name) VALUES(?,?,?)"
                         .format(self.id), (item_name, unit, mnn,))
        self.conn.commit()
        return self.cur.lastrowid

    def add_quantity(self, id_item, quant, quant_sign, date, doc):  # добавляем приход, расход (с минусом в quant_sign)
        if not quant_sign:
            quant *= -1
            self.cur.execute("INSERT INTO division(name) VALUES(?)", (doc,))

        self.cur.execute("INSERT INTO quantity{}(item_id, quantity,date_of_insert,doc) VALUES(?,?,?,?)".format(self.id),
                         (id_item, quant, date, doc,))
        self.conn.commit()

    def show_package(self):  # возвращаем Упаковки
        try:
            return self.cur.execute('''SELECT name FROM units''').fetchall()
        except:
            return []

    def show_division(self):  # возвращаем отделения
        try:
            return self.cur.execute('''SELECT name FROM division''').fetchall()
        except:
            return []


    def show_mnn(self):  # возвращаем мнн
        try:
            return self.cur.execute('''SELECT name FROM mnn''').fetchmany(1000000)
        except:
            return []


    def show_data(self):  # возвращаем 10000  записей товара
        try:
            return self.cur.execute('''SELECT id, name, unit, mnn_name FROM items{} ORDER BY id ASC'''
                                    .format(self.id)).fetchall()
        except:
            return []

    def show_data_order_by_name(self):  # возвращаем 10000  записей товара в алфавитном порядке
        try:
            return self.cur.execute('''SELECT id, name, unit, mnn_name FROM items{} ORDER BY name ASC'''
                                    .format(self.id)).fetchall()
        except:
            return []


    def delete_quantity(self, quant_id):  # удаляем проиход/расход
        self.cur.execute("DELETE from quantity{} where id = {}".format(self.id, quant_id))
        self.conn.commit()

    def delete_all_quantity_item(self, item_id):
        self.cur.execute("DELETE from quantity{} where item_id = {}".format(self.id, item_id))
        self.conn.commit()

    def delete_item(self, item_id):  # удаляем товар
        self.cur.execute("DELETE from items{} where id = {}".format(self.id, item_id))
        self.cur.execute("DELETE from quantity{} where item_id = {}".format(self.id, item_id))
        self.conn.commit()

    def calculate_items(self, item_id):  # возвращаем остаток товара
        return \
            self.cur.execute('''SELECT sum(quantity) FROM quantity{} WHERE item_id = {}'''
                             .format(self.id, item_id)).fetchone()[0]


    def import_from_xls(self, file_name, date_today):  # импортируем из экселя
        p = XlsxImport(file_name)
        data = p.import_into_list()
        del p
        for i in data:
            b = self.add_items(i[0], i[1])
            info = self.cur.execute('SELECT * FROM items{} WHERE id=?'.format(self.id), (b,))
            if info.fetchone() is None:
                return
            else:
                self.add_quantity(b, i[2], True, date_today, '')

    def import_from_ods(self, file_name, date_today):  # импортируем из ods
        p = OdsExport()
        data = p.export_from_ods(file_name)
        print(data)
        del p
        for i in data:
            b = self.add_items(i[0], i[1])
            info = self.cur.execute('SELECT * FROM items{} WHERE id=?'.format(self.id), (b,))
            if info.fetchone() is None:
                return
            else:
                self.add_quantity(b, i[2], True, date_today, '')

    def select_quant_by_date(self, from_date, to_date):  # возвращаем проиход/расход товара за период времени
        return self.cur.execute(
            '''SELECT * FROM quantity{} LEFT JOIN items{} ON quantity{}.item_id = items{}.id
                                    WHERE date_of_insert BETWEEN "{}" AND "{}"'''
            .format(self.id, self.id, self.id, self.id, from_date, to_date)).fetchall()

    def show_quantyty_by_id_date(self, id_item, from_date, to_date):
        return self.cur.execute(
            '''SELECT * FROM quantity{} 
                WHERE date_of_insert BETWEEN "{}" AND "{}"
                AND item_id = {}'''.format(self.id, from_date, to_date, id_item)).fetchall()

    def show_quantyty_by_division_date(self, doc, from_date, to_date):
        return self.cur.execute(
            '''SELECT item_id, name, unit, quantity FROM quantity{} LEFT JOIN items{} ON quantity{}.item_id = items{}.id
                WHERE  date_of_insert BETWEEN "{}" AND "{}"
                AND doc = "{}"'''.format(self.id, self.id, self.id, self.id, from_date, to_date,  doc)).fetchall()

    def return_residue(self):  # считает остатки по всем позициям
        all_residue = []
        for a in self.show_data_order_by_name():
            one_residue = [a[1], a[2], a[3], str(self.calculate_items(a[0]))]
            all_residue.append(one_residue)

        return all_residue

    def show_data_of_groups(self):  # возвращаем 10000  записей товара
        return self.cur.execute('''SELECT id, name FROM groups ORDER BY id ASC''').fetchmany(10000)

    def get_id_from_items(self, item_name):
        return self.cur.execute(
            '''SELECT id FROM items{} 
                        WHERE name = ? '''.format(self.id), (item_name,)).fetchone()



# t = DataBase()
# t.delete_group(6)
# t.id = 2
# pprint(t.return_residue())
# t.add_items('Афобазол', "упаковка", "афик")
# print(t.show_data_of_groups(32))
# t.change_item(1, 'лох', "пидр",'чмо')
# print(t.show_item_by_id(32))
# print()
# t.create_group('пенис')
# t.import_from_xls('wb1.xlsx', date.today())
# t.add_quantity(1, 10, False, '2022-06-14', 'Инфекционное')
# t.delete_item(9)
# print(t.calculate_items(1))
# print(t.select_quant_by_date("2022-06-14", "2023-08-31"))
# print(t.show_quantyty_by_id_date(1,"2022-06-14", "2023-08-31"))
