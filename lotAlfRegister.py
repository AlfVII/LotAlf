# -*- coding: utf-8 -*-

class Register():
    def __init__(self):

        # self.collections = LoadCollectionsFromDB()
        self.collections = [{'name': 'Colección de Alfonso',
                             'data': {
                                      '12369': { 'status': 'Doblado',
                                                'year': '1986',
                                                'coin': 'Euro',
                                                'administration': {'province': 'Jaén',
                                                                   'town': 'Navas de San Juan',
                                                                   'number': '1' 
                                                                  }
                                                },
                                      '00001': { 'status': 'Doblado',
                                                'year': '1986',
                                                'coin': 'Euro',
                                                'administration': {'province': 'Jaén',
                                                                   'town': 'Navas de San Juan',
                                                                   'number': '1' 
                                                                  }
                                                }
                                     }
                            },
                            {'name': 'Colección de Alfonso2',
                             'data': {}
                            }
                           ]

    def get_number_data(self, collection_index, number):
        if str('{:05d}'.format(number)) in self.collections[collection_index]['data']:
            return self.collections[collection_index]['data'][str('{:05d}'.format(number))]
        else:
            return None
        return None

    def get_collections(self):
        return self.collections

    def get_collections_names(self):
        collections = []
        for collection in self.collections:
            collections.append(collection['name'])
        return collections

    def add_to_collection(self, collection_index, collection_key, datum):
        if collection_key not in self.collections[collection_index]['data']:
            self.collections[collection_index]['data'][collection_key] = datum
        else:
            return 0
        return 1

    def save_to_collection(self, collection_index, collection_key, datum):
        print(collection_index)
        print(str('{:05d}'.format(collection_key)))
        print(datum)
        self.collections[collection_index]['data'][str('{:05d}'.format(collection_key))] = datum
        return 1
