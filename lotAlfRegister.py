# -*- coding: utf-8 -*-
import glob
import sqlite3
import os
from sqlite3 import Error
from string import maketrans

class Register():
    def __init__(self):

        self.filters = {}

        print(os.path.expanduser('~/collections.db'))

        try:
            self.collections = sqlite3.connect(os.path.expanduser('~/collections.db'))
            self.collections.text_factory = str
        except Error as e:
            print(e)

    def __del__(self):
        self.collections.close()

    def get_number_data(self, collection_index, number):
        collection = self.get_collection_name(collection_index)
        print("collection")
        print(collection)
        sql = "SELECT * FROM {} WHERE number={};".format(collection, number)
        print(collection)

        try:
            c = self.collections.cursor()
            c.execute(sql)
            data = c.fetchall()
        except Error as e:
            print(e)

        print("data")
        print(data)
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

    def get_filtered_data(self, collection_index, where_clause):
        collection = self.get_collection_name(collection_index)
        sql = "SELECT number FROM {} {};".format(collection, where_clause)

        print(sql)
        try:
            c = self.collections.cursor()
            c.execute(sql)
            data = c.fetchall()
        except Error as e:
            print(e)

        filtered_numbers = []
        for datum in data:
            filtered_numbers.append(datum[0])

        return filtered_numbers

    def get_count_filtered_data(self, collection_index, column_name, where_clause='', group=True):
        collection = self.get_collection_name(collection_index)
        if group:
            groupby_clause = " GROUP BY {0}".format(column_name)
        else:
            groupby_clause = ''
        sql = "SELECT COUNT({0}) AS count_{0}, {0} FROM {1} {2} {3};".format(column_name, collection, where_clause, groupby_clause)

        print(sql)
        try:
            c = self.collections.cursor()
            c.execute(sql)
            data = c.fetchall()
        except Error as e:
            print(e)

        return data


    def apply_filters(self, collection):
        where_clause = " WHERE "
        empty = True
        for key, value in self.filters.iteritems():
            if value != '':
                print(value)
                empty = False
                where_clause += value
                where_clause += ' AND '

        if where_clause[-5:] == ' AND ':
            where_clause = where_clause[:-5]

        if empty:
            where_clause = ''

        return self.get_filtered_data(collection, where_clause)


    def set_filter(self, field, filter):
        self.filters[field] = filter
