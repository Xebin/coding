__author__ = 'xebin'

import json
import uuid

def save_json(save_path, data):
    # print 'save to:', save_path
    with open(save_path, 'w') as f:
        json.dump(data, f)

def dump_coors(data):
    id = uuid.uuid4()
    base = '/Users/jiusi/Desktop/'
    data = data.tolist()
    save_json(base + str(id), data)


def load_data(load_path):
    with open(load_path, 'r') as f:
        return json.load(f)