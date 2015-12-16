#! /bin/python
#
#   Grabs characters and organizes them with works
#
##########################################

from bs4 import BeautifulSoup as bS
import io
from pathlib import Path

ROOTDIR = "../fetch/"
HTMDIR = "charDataHTML/"
BOOKSDIR = "CalliSources/books/"
CHARDIR = "CalliSources/characterimage/"
OUTDIR = "/home/dave/workspace/pycharm/CADAL-work/works/"


class Character(object):
    mark = ""
    author = ""
    work = ""
    work_id = ""
    page_id = ""
    file_name = ""
    image = bytearray()

def grabcharsfromfile(htmlfile):
    charfile = open(htmlfile)
    char_bs = bS(charfile, "lxml")
    charfile.close()
    chartable = char_bs.table  # All characters exist in the same table
    characterblocks = chartable.findAll("p")
    numchars = len(characterblocks) // 4
    curspot = 0
    characters = []
    for x in range(0, numchars):
        char = Character()
        char.mark = characterblocks[curspot].contents[1].string
        curspot += 1
        charauthorblock = characterblocks[curspot].string
        if len(charauthorblock) > 4:  # we have an author
            char.author = charauthorblock[4::]
        curspot += 1
        charworkblock = characterblocks[curspot].string
        if len(charworkblock) > 3:
            char.work = charworkblock[3::]
        curspot += 1
        characterblocks[curspot].unwrap()
        filepathname = characterblocks[curspot].attrs['id']
        char.work_id = filepathname[:8]
        char.page_id = filepathname[19:26]
        char.file_name = filepathname[18:]
        curspot += 1
        charimagefile = open(ROOTDIR + CHARDIR + char.work_id + "/" + char.file_name, "rb")
        char.image = charimagefile.read()
        charimagefile.close()
        characters.append(char)
    return characters,

def buildpagefromfile(htmlfile):
    charpage = grabcharsfromfile(htmlfile)[0]
    for char in charpage:
        imagedir = ROOTDIR + BOOKSDIR + char.work_id
        p = Path(imagedir)
        if not p.is_dir():
            print(char)




for curfile in range(1, 5500):  # 5500
    filename = ROOTDIR + HTMDIR + str(curfile) + ".html"
    buildpagefromfile(filename)


