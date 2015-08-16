
import os
import fnmatch

FILE = 0
DIR = 1
FILE_AND_DIR = 2

def glob(path='./', pattern='*', node_type=FILE):
    path = os.path.normpath(path)
    contents = os.listdir(path)

    if node_type == FILE:
        filt = lambda x: os.path.isfile(x)
    elif node_type == DIR:
        filt = lambda x: os.path.isdir(x)
    else:
        filt = lambda x: True
    contents = [c for c in contents if filt(x) is True]

    return fnmatch.filter(contents, pattern)
