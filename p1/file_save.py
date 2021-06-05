import numpy as np


def save(data):
    np.savez('./data/data.npz', data=data)


def read():
    data = np.load('./data/data.npz')
    all_d = data['data']
    data.close()
    return all_d
