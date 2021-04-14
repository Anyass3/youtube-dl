import os
import json
from typing import Optional, Dict


class Store:
    def __init__(self):
        if not os.path.exists('store.json'):
            with open('store.json', 'w') as f:
                store = {'downloading': []}
                json.dump(store, f)

    def set(self, value):
        with open('store.json', 'w') as f:
            json.dump(value, f)

    @property
    def value(self):
        with open('store.json') as f:
            return json.load(f)

    @property
    def downloads(self):
        return self.value['downloading']

    def downloading(self, val, add=True):
        store_value: Dict[str, any] = self.value
        downloading = set(store_value['downloading'])
        if add:
            downloading.add(val)
        else:
            downloading.remove(val)
        store_value['downloading'] = list(downloading)
        self.set(store_value)


store = Store()
