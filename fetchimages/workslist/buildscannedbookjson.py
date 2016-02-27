#
#
#  Parses info from scanned books, and builds importable json
#
################################################################

import socket

if socket.gethostname() == 'bigArch':
    CHARS_DIR = "/home/dave/workspace/pycharm/fetch/scanned/1/"
else:
    CHARS_DIR = "/media/scanned/1/"


class Work(object):
    def __init__(self, wkid, int, title: str):
        self.wkid = wkid
        self.title = title


class Page(object):
    def __init__(self, ):



# 3109 is next available primary key in works
wk = Work(wkid=4109, title="集字聖教序, 三島")