#! /bin/python
#
#   Grabs characters and organizes them with works
#
##########################################

from bs4 import BeautifulSoup as bS
from pathlib import Path
from urllib import request
import sys, pickle
from io import FileIO

ROOTDIR = "../fetch/"
HTMDIR = "charDataHTML/"
BOOKSDIR = "CalliSources/books/"
CHARDIR = "CalliSources/characterimage/"
CADALWEBSITE = "http://www.cadal.zju.edu.cn/CalliSources/images/books/"


class Character(object):
    htmlpage = int()
    mark = ""
    author = ""
    work = ""
    work_id = ""
    page_id = ""
    file_name = ""
    image = bytearray()


def grabcharsfromfile(htmlfile, cur_file):
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
        char.htmlpage = cur_file
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
        char.page_id = filepathname[18:26]
        char.file_name = filepathname[18:]
        curspot += 1
        charimagefile = open(ROOTDIR + CHARDIR + char.work_id + "/" + char.file_name, "rb")
        char.image = charimagefile.read()
        charimagefile.close()
        characters.append(char)
    return characters,

def printcharinfo(char):
    print("Mark: " + char.mark)
    print("HTML Source: " + str(char.htmlpage))
    print("work_id: " + char.work_id)
    print("page_id: " + char.page_id)
    print("----------------------------------------------------------------------")

def grabfile(webaddress):
    url = request.urlopen(webaddress)
    gotimage = url.read()
    url.close()
    return gotimage


def checkfilesanddirs(char):
    imagedir = ROOTDIR + BOOKSDIR + char.work_id
    if not Path(imagedir).is_dir():
        print("Directory does not exist for this work!")
        printcharinfo(char)
    else:
        imagename = imagedir + "/" + char.page_id + ".jpg"
        imagepath = Path(imagename)
        if not imagepath.is_file():
            printcharinfo(char)
            webaddress = CADALWEBSITE + char.work_id + "/" + char.page_id + ".jpg"
            print("Downloading: " + webaddress + "\n.....")
            try:
                gotimage = grabfile(webaddress)
                imagepath.write_bytes(gotimage)
            except:
                print(sys.exc_info()[0])
                input("try to trigger image generation manually please")
                try:
                    gotimage = grabfile(webaddress)
                    imagepath.write_bytes(gotimage)
                except:
                    print(sys.exc_info()[0])
                    print("Download failed again")
            print("-----------------------------------------")

EXPECTED_CHARS_PER_PAGE = 18

def checkcharsinpage(charpage, fileNo):
    clen = len(charpage)
    if clen != EXPECTED_CHARS_PER_PAGE:
     print(str(clen) + " Characters detected in file " + str(fileNo) + ".html")

def buildpagefromfile(htmlfile, curfile):
    charpage = grabcharsfromfile(htmlfile, curfile)[0]
    return charpage

character_set = []
for curfile in range(1, 5500):  # 5500
    filename = ROOTDIR + HTMDIR + str(curfile) + ".html"
    character_set.append(buildpagefromfile(filename, curfile))

pickle_file = FileIO.

pickle.dump(character_set, FileIO., protocol=pickle.HIGHEST_PROTOCOL, fix_imports=False)

