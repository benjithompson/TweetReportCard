"""Handles file read/write, pickling and user input"""

import os
import pickle

def get_path(filename, folder='', ext=''):
    """Utility function to create file paths"""
    path = os.getcwd() + folder
    filename = os.path.join(path, filename + ext)
    return filename

def save_data_to_file(data, filename):
    """iterates through all posts and comments and writes them to specified file"""

    try:
        if __verify_write(filename):
            __write_data(data, filename)
        else:
            print('aborting file write...')
    except OSError as err:
        print(err.strerror)

def __verify_write(filename):
    """Return true if user wants to overwrite existing file"""

    if os.path.exists(filename):
        ans = input(filename + ' already exists. Overwrite? (y/n): ')
        return ans == 'y' or ans == 'Y'
    else:
        ans = input('Do you really want to write to ' + filename + '(y/n)?: ')
        return ans == 'y' or ans == 'Y'

def __write_data(data, filename):
    try:
        pickle.dump(data, open(filename, "wb"))
        print('pickle successfully written')
    except pickle.PickleError as perr:
        print(perr)

def read_from_file(filename):
    """read file into string"""

    text = ''

    with open(filename, 'r') as f:
        for line in f.readline():
            text += line

    return text

def load_pickle(path):
    """opens object from pickle file at path"""

    data = None

    try:
        data = pickle.load(open(path, 'rb'))

    except pickle.UnpicklingError as perr:
        print(perr)

    except FileNotFoundError as fnfe:
        print(fnfe)

    return data
        