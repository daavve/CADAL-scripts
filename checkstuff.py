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
    def __init__(self, mark: str, author: str, work: str, work_id: str, page_id: str, coordinates: List[str]):
        self.chi_mark = mark
        self.chi_author = author
        self.chi_work = work
        self.work_id = work_id
        self.page_id = page_id
        self.xy_coordinates = coordinates


class Charfile(object):
    def __init__(self, work_id: str, page_id: str, coordinates: List[str]):
        self.work_id = work_id
        self.page_id = page_id
        self.xy_coordinates = coordinates


class Page(object):
    def __init__(self, work_id: str, page_id: str):
        self.work_id = work_id
        self.page_id = page_id


def readjson(filename: str) -> List[Character]:  # Not too bad, less than 70M
    jsonfile = open("dump.json", "r")
    readfile = json.load(jsonfile)
    jsonfile.close()
    characters = []
    for r in readfile:
        characters.append(
            Character(r['chi_mark'], r['chi_author'], r['chi_work'], r['work_id'], r['page_id'], r['xy_coordinates']))
    return characters


def loadcharlist() -> List[Charfile]:
    charfiles = []
    for f in os.listdir(ROOTDIR + CHARDIR):
        pathname = os.path.join(ROOTDIR + CHARDIR, f)
        booknum = str(pathname).split('/')[4]
        if S_ISDIR(os.stat(pathname).st_mode):
            for img in os.listdir(pathname):
                if img.endswith('.jpg'):
                    imgs = img.split('(')
                    pagenum = imgs[0]
                    coords = imgs[1].strip(').jpg').split(',')
                    charfiles.append(Charfile(booknum, pagenum, coords))
    return charfiles


def loadimagelist() -> List[Page]:  # I know cut / paste coding is bad, but i'm in a hurry
    imgfiles = []
    for f in os.listdir(ROOTDIR + BOOKSDIR):
        pathname = os.path.join(ROOTDIR + BOOKSDIR, f)
        booknum = str(pathname).split('/')[4]
        if S_ISDIR(os.stat(pathname).st_mode):
            for img in os.listdir(pathname):
                if img.endswith('.jpg'):
                    imgname = img.strip('.jpg')
                    imgfiles.append(Page(booknum, imgname))
    return imgfiles


def setseq(char: Character, chfile: Charfile) -> bool:
    a = char.xy_coordinates
    b = chfile.xy_coordinates

    if a[0] == b[0] and a[1] == b[1] and a[2] == b[2] and a[3] == b[3]:
        return True
    else:
        return False


# Note, search not at all efficient, but I only do it once
def print_data_chars_with_no_file(jchars: Character, fchars: Charfile) -> None:
    for jchar in jchars:
        found = False
        for fchar in fchars:
            if jchar.work_id == fchar.work_id and jchar.page_id == fchar.page_id and setseq(jchar, fchar):
                found = True
        if not found:
            print(str(jchar.work_id) + " " + str(jchar.page_id) + " " + str(jchar.xy_coordinates))  # This should not happen


# Note, search not at all efficient, but I only do it once
def print_file_chars_with_no_data(jchars: Character, fchars: Charfile) -> None:
    for fchar in fchars:
        found = False
        for jchar in jchars:
            if jchar.work_id == fchar.work_id and jchar.page_id == fchar.page_id and setseq(jchar, fchar):
                found = True
        if not found:
            print(str(fchar.work_id) + " " + str(fchar.page_id) + " " + str(fchar.xy_coordinates))  # This should not happen



# Reads the json dump I was able to get from the website

charsj = readjson('dump.json')
print("number of non-null characters on website: " + str(charsj.__len__()))

# Walks through the charlist dir and gets a list of all images we have

charsf = loadcharlist()
print("number of individual characters from website: " + str(charsf.__len__()))

# Walks through the work dir and gets a record of all books & pages of books we have.

imgsf = loadimagelist()
print("number of pages of books from website: " + str(imgsf.__len__()))

# print_data_chars_with_no_file(charsj, charsf)

print_file_chars_with_no_data(charsj, charsf)
