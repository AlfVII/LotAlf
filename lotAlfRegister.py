# -*- coding: utf-8 -*-
import glob
import sqlite3
from sqlite3 import Error
from string import maketrans

class Register():
    def __init__(self):


        try:
            self.collections = sqlite3.connect('collections.db')
            self.collections.text_factory = str
        except Error as e:
            print(e)

    def __del__(self):
        self.collections.close()

    def get_number_data(self, collection_index, number):
        collection = self.get_collection_name(collection_index)
        sql = "SELECT * FROM {} WHERE number={};".format(collection, number)

        try:
            c = self.collections.cursor()
            c.execute(sql)
            data = c.fetchall()
        except Error as e:
            print(e)

        datadict = {}
        if len(data) > 0:
            for idx, col in enumerate(c.description):
                datadict[col[0]] = data[0][idx]

            return datadict
        else:
            return None

    def get_number_collections(self):
        sql = "SELECT name FROM sqlite_master WHERE type='table';"

        try:
            c = self.collections.cursor()
            c.execute(sql)
            tables = c.fetchall()
        except Error as e:
            print(e)

        return len(tables)

    def new_collection(self, name, fill):
        sql = """ CREATE TABLE IF NOT EXISTS {} (
                                        number integer PRIMARY KEY,
                                        status text NOT NULL,
                                        origin text,
                                        lot text,
                                        year text,
                                        coin text,
                                        administration_province text,
                                        administration_town text,
                                        administration_number text,
                                        copies integer NOT NULL
                                    ); """.format(name)

        try:
            c = self.collections.cursor()
            c.execute(sql)
        except Error as e:
            print(e)

        if fill:
            for i in range(0, 100000):
                datum = {'number': i, 
                         'status': 'Perfecto', 
                         'year': None, 
                         'coin': None, 
                         'lot': None, 
                         'administration_province': None, 
                         'administration_town': None, 
                         'administration_number': None, 
                         'origin': None, 
                         'copies': 1}


                columns = ', '.join(datum.keys())
                placeholders = ':'+', :'.join(datum.keys())
                sql = 'INSERT INTO {} ({}) VALUES ({})'.format(name, columns, placeholders)
                c.execute(sql, datum)

            self.collections.commit()

    def get_collections_names(self):
        sql = "SELECT name FROM sqlite_master WHERE type='table';"

        try:
            c = self.collections.cursor()
            c.execute(sql)
            tables = c.fetchall()
        except Error as e:
            print(e)

        name = []
        for table in tables:
            name.append(table[0])

        return name

    def get_collection_name(self, index):
        sql = "SELECT name FROM sqlite_master WHERE type='table';"

        try:
            c = self.collections.cursor()
            c.execute(sql)
            tables = c.fetchall()
        except Error as e:
            print(e)

        return tables[index][0]

    def add_to_collection(self, collection_index, datum):
        collection = self.get_collection_name(collection_index)
        c = self.collections.cursor()

        for key, value in datum.items():
            if value == '':
                datum[key] = None

        columns = ', '.join(datum.keys())
        placeholders = ':'+', :'.join(datum.keys())
        sql = 'INSERT INTO {} ({}) VALUES ({})'.format(collection, columns, placeholders)

        c.execute(sql, datum)
        self.collections.commit()
        if c.lastrowid is None:
            return 0
        else:
            return 1

    def update_collection(self, collection_index, number, datum):
        collection = self.get_collection_name(collection_index)

        sql = "UPDATE {} SET ".format(collection)
        for key, value in datum.items():
            if isinstance(value, str):
                if value == '':
                    sql += "{} = NULL, ".format(key, value)
                else:
                    sql += "{} = '{}', ".format(key, value)
            else:
                sql += "{} = {}, ".format(key, value)

        sql = sql[:-2]
        sql += " WHERE number = {};".format(number)

        c = self.collections.cursor()
        c.execute(sql)
        self.collections.commit()
        return c.rowcount > 0
