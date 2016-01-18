#! /bin/python
#
#   Grabs characters and organizes them with works
#
##########################################

from bs4 import BeautifulSoup as bS
from pathlib import Path
from urllib import request
from typing import List
import sys, json

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


def splitcoordinates(infilename: str) -> List[str]:  # Input 00000172(791,82,857,172).jpg, output [791,82,857,172]
    lastpart = infilename[8:]
    slastpart = lastpart.strip("().jpg")
    coords = slastpart.split(",")
    return coords


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
        coords = splitcoordinates(filepathname[18:])
        curspot += 1
        characters.append(Character(mark, author, work, work_id, page_id, coords))
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


def jdefault(o):
    return o.__dict__


def dumpjsontofile(charset: List[Character]) -> None:
    character_list = []
    for charpage in charset:
        for char in charpage:
            character_list.append(char)
    dumpfile = open("dump.json", "w")
    json.dump(character_list, dumpfile, ensure_ascii=False, indent=4, sort_keys=True, default=jdefault)
    dumpfile.close()


def readjsonfromfile() -> List[Character]:
    jsonfile = open("dump.json", "r")
    readfile = json.load(jsonfile)
    jsonfile.close()
    character_set = []
    for r in readfile:
        character_set.append(Character(r['chi_mark'],
                                       r['chi_author'],
                                       r['chi_work'],
                                       r['work_id'],
                                       r['page_id'],
                                       r['xy_coordinates']))
    return character_set


def parsecharsfromhtml() -> List[Character]:
    character_set = []
    for curfile in range(1, 5500):  # 5500      This part uses about 3.2 GB of RAM :(
        filename = ROOTDIR + HTMDIR + str(curfile) + ".html"
        character_set.append(buildpagefromfile(filename, curfile))
    return character_set


def countworkid(charset: List[Character]) -> None:
    workset = []
    for char in charset:
        if char.work_id not in workset:
            workset.append(char.work_id)
    workset.sort()
    print(workset)

charset = readjsonfromfile()    # This part uses less than 150mb, Probably won't use Database till I have to
input('press enter to continue')

