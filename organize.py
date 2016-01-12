#! /bin/python
#
#   Grabs characters and organizes them with works
#
##########################################

from bs4 import BeautifulSoup as bS
from pathlib import Path
from urllib import request
from io import FileIO
from typing import List
import sys

ROOTDIR = "../fetch/"
HTMDIR = "charDataHTML/"
BOOKSDIR = "CalliSources/books/"
CHARDIR = "CalliSources/characterimage/"
CADALWEBSITE = "http://www.cadal.zju.edu.cn/CalliSources/images/books/"


class Character(object):
        def __init__(self, mark: str, author: str, work: str, work_id: str, page_id: str, file_name: str):
            self.mark = mark
            self.author = author
            self.work = work
            self.work_id = work_id
            self.page_id = page_id  # FileName = ROOTDIR + CHARDIR + work_id + "/" + file_name
            self.file_name = file_name


def grabcharsfromfile(htmlfile: str, cur_file: int) -> List[Character]:
    charfile = open(htmlfile)
    char_bs = bS(charfile, "lxml")
    charfile.close()
    chartable = char_bs.table  # All characters exist in the same table
    characterblocks = chartable.findAll("p")
    numchars = len(characterblocks) // 4
    curspot = 0
    characters = []
    for x in range(0, numchars):
        mark = characterblocks[curspot].contents[1].string
        curspot += 1
        charauthorblock = characterblocks[curspot].string
        if len(charauthorblock) > 4:  # we have an author
            author = charauthorblock[4::]
        else:
            author = ""
        curspot += 1
        charworkblock = characterblocks[curspot].string
        if len(charworkblock) > 3:
            work = charworkblock[3::]
        else:
            work = ""
        curspot += 1
        characterblocks[curspot].unwrap()
        filepathname = characterblocks[curspot].attrs['id']
        work_id = filepathname[:8]
        page_id = filepathname[18:26]
        file_name = filepathname[18:]
        curspot += 1
        characters.append(Character(mark, author, work, work_id, page_id, file_name))
    return characters,


def printcharinfo(char: str) -> None:
    print("Mark: " + char.mark)
    print("HTML Source: " + str(char.htmlpage))
    print("work_id: " + char.work_id)
    print("page_id: " + char.page_id)
    print("----------------------------------------------------------------------")


def grabfile(webaddress: str) -> str:
    url = request.urlopen(webaddress)
    gotimage = url.read()
    url.close()
    return gotimage


def checkfilesanddirs(char: Character) -> None:
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


def checkcharsinpage(charpage: List[Character], fileno: int) -> None:
    clen = len(charpage)
    if clen != EXPECTED_CHARS_PER_PAGE:
     print(str(clen) + " Characters detected in file " + str(fileno) + ".html")


def buildpagefromfile(htmlfile: str, curfile1: int) -> List[Character]:
    charpage = grabcharsfromfile(htmlfile, curfile1)[0]
    return charpage




character_set = []
for curfile in range(1, 5500):  # 5500      This part uses about 3.2 GB of RAM :(
    print("Reading html file: " + str(curfile) + " of 5500")
    filename = ROOTDIR + HTMDIR + str(curfile) + ".html"
    character_set.append(buildpagefromfile(filename, curfile))

input("press enter to continue")
# Can't do Pickle of Character Object.  It takes up lots of memory and even more disk space

