#! /bin/python
#
#   Checks chardata against downloaded data
#
##########################################

from typing import List
from pathlib import Path
import json, os, sys
from stat import *

ROOTDIR = "../fetch/"
HTMDIR = "charDataHTML/"
BOOKSDIR = "CalliSources/books/"
CHARDIR = "CalliSources/characterimage/"
CADALWEBSITE = "http://www.cadal.zju.edu.cn/CalliSources/images/books/"


class Character(object):
    def __init__(self, mark: str,
                       author: str,
                       work: str,
                       work_id: str,
                       page_id: str,
                       coordinates: List[str]):
        self.chi_mark = mark
        self.chi_author = author
        self.chi_work = work
        self.work_id = work_id
        self.page_id = page_id
        self.xy_coordinates = coordinates


class Charfile(object):
    def __init__(self, work_id: str,
                       page_id: str,
                       coordinates: List[str]):
        self.work_id = work_id
        self.page_id = page_id
        self.xy_coordinates = coordinates


class Page(object):
    def __init__(self, work_id: str,
                       page_id: str):
        self.work_id = work_id
        self.page_id = page_id


def readjson(filename : str) -> List[Character]:    # Not too bad, less than 70M
    jsonfile = open("dump.json", "r")
    readfile = json.load(jsonfile)
    jsonfile.close()
    characters = []
    for r in readfile:
        characters.append(Character(r['chi_mark'],
                                       r['chi_author'],
                                       r['chi_work'],
                                       r['work_id'],
                                       r['page_id'],
                                       r['xy_coordinates']))
    return characters


def loadcharlist() -> List[Charfile]:
    charfiles = []
    for f in os.listdir(ROOTDIR + CHARDIR):
        pathname = os.path.join(ROOTDIR + CHARDIR, f)
        if S_ISDIR(os.stat(pathname).st_mode):
            for img in os.listdir(pathname):
                if img.endswith('.jpg'):
                    imgs = img.split('(')
                    pagenum = imgs[0]
                    coords = imgs[1].strip(').jpg').split(',')
                    charfiles.append(Charfile(pathname,
                                              pagenum,
                                              coords))
    return charfiles

def loadimagelist() -> List[Page]:  # I know cut / paste coding is bad, but i'm in a hurry
    imgfiles = []
    for f in os.listdir(ROOTDIR + BOOKSDIR):
        pathname = os.path.join(ROOTDIR + BOOKSDIR, f)
        if S_ISDIR(os.stat(pathname).st_mode):
            for img in os.listdir(pathname):
                if img.endswith('.jpg'):
                    imgname = img.strip('.jpg')
                    imgfiles.append(Page(pathname, imgname))
    return imgfiles


charsj = readjson('dump.json')
charsf = loadcharlist()
imgsf = loadimagelist()
loadimagelist()
input('...')



