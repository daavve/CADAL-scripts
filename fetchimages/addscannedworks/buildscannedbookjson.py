#
#
#  Parses info from scanned books, and builds importable json
#
################################################################

import socket
import json
import os

if socket.gethostname() == 'bigArch':
    SCANNED_DIR = "/home/dave/workspace/pycharm/fetch/scanned/1/"
else:
    SCANNED_DIR = "/media/scanned/1/"


class Work(object):
    def __init__(self, wkid: int, title: str, author: str):
        self.wkid = wkid
        self.title = title
        self.author = author
        self.pages = []


class Page(object):
    def __init__(self, filepath: str, transcript: str):
        self.filepath = filepath
        self.transcript = transcript



def jdefault(o):    # This part is necessary to get the objects to Auto-Format
    return o.__dict__


def dumptojson() -> None:
    dumpfile = open('scannedwork1.json', mode='w')
    json.dump(wk, dumpfile, ensure_ascii=False, indent=4, sort_keys=True, default=jdefault)
    dumpfile.close()

# 3109 is next available primary key in works
wk = Work(wkid=int(4109), title="集字聖教序, 三島", author="王羲之")

file = open("tesseract_convert.txt", mode="r", encoding="utf-8")
redfile = file.read()
file.close()

textbody = redfile.split('##########################################\n\n')[1]
textbody = textbody.split('\n\n\nSTOP!')[0]
textlist = textbody.split('\n\n-----------------------\n')
for text in textlist:
    filepath = SCANNED_DIR + text.split('\n')[0]
    if not os.path.isfile(filepath):
        Exception("File not found", filepath)
    filetext = text.split('.png\n')[1]
    wk.pages.append(Page(filepath=filepath, transcript=filetext))
dumptojson()