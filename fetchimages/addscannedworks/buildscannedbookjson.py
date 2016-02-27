#
#
#  Parses info from scanned books, and builds importable json
#
################################################################

import socket
import json

if socket.gethostname() == 'bigArch':
    CHARS_DIR = "/home/dave/workspace/pycharm/fetch/scanned/1/"
else:
    CHARS_DIR = "/media/scanned/1/"


class Work(object):
    def __init__(self, wkid, int, title: str, author: str):
        self.wkid = wkid
        self.title = title
        self.author = author
        self.pages = []


class Page(object):
    def __init__(self, filepath: str, tanscript: str):
        self.filepath = filepath
        self.transcript = tanscript



def jdefault(o):    # This part is necessary to get the objects to Auto-Format
    return o.__dict__


def dumptojson() -> None:
    dumpfile = open('dump2.json', mode='w')
    json.dump(wk, dumpfile, ensure_ascii=False, indent=4, sort_keys=True, default=jdefault)
    dumpfile.close()

# 3109 is next available primary key in works
wk = Work(wkid=4109, title="集字聖教序, 三島", author="王羲之")

file = open("tesseract_convert.txt", mode="r", encoding="utf-8")
redfile = file.read()
file.close()

