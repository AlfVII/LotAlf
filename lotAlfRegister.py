# -*- coding: utf-8 -*-
import glob
import yaml


class Register():
    def __init__(self):

        self.collections = self.load_collections()

    def get_number_data(self, collection_index, number):
        if str('{:05d}'.format(number)) in self.collections[collection_index]['data']:
            return self.collections[collection_index]['data'][str('{:05d}'.format(number))]
        else:
            return None
        return None

    def get_collections(self):
        return self.collections

    def new_collection(self, name, fill):
        collection = {'name': name, 'data': {}}
        if fill:
            for i in range(0, 100000):
                print(i)
                collection['data'][str('{:05d}'.format(i))] = {'status': 'Perfecto',
                                                               'year': '',
                                                               'coin': '',
                                                               'lot': '',
                                                               'administration': {'province': '',
                                                                                  'town': '',
                                                                                  'number': '' 
                                                                                 },
                                                               'origin': '',
                                                               'copies': 1
                                                               }
        self.save_collection(collection)
        self.collections = self.load_collections()

    def get_collections_names(self):
        collections = []
        for collection in self.collections:
            collections.append(collection['name'].encode('utf-8'))
        return collections

    def add_to_collection(self, collection_index, collection_key, datum):
        if collection_key not in self.collections[collection_index]['data']:
            self.collections[collection_index]['data'][collection_key] = datum
            self.save_collection(self.collections[collection_index])
        else:
            return 0
        return 1

    def save_to_collection(self, collection_index, collection_key, datum):
        print(collection_index)
        print(str('{:05d}'.format(collection_key)))
        print(datum)
        self.collections[collection_index]['data'][str('{:05d}'.format(collection_key))] = datum
        self.save_collection(self.collections[collection_index])
        return 1

    def load_collections(self):
        collections_yaml = glob.glob("*.yaml")
        collections = []
        for collection in collections_yaml:
            with open(collection, 'r') as stream:
                try:
                    collections.append(yaml.load(stream))
                except yaml.YAMLError as exc:
                    print(exc)

        return collections

    def save_collection(self, collection):
        with open('{}.yaml'.format(collection['name'].encode('utf-8')), 'w') as outfile:
            yaml.dump(collection, outfile, default_flow_style=False, encoding=('utf-8'), allow_unicode=True)
