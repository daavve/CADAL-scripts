#! /bin/python
#
#   Grabs characters and organizes them with works
#
##########################################

from bs4 import BeautifulSoup as bS
import io

ROOTDIR = "../fetch/"
HTMDIR = "charDataHTML/"
BOOKSDIR = "CalliSources/books/"
CHARDIR = "CalliSources/characterimage/"
OUTDIR = "/home/dave/workspace/pycharm/CADAL-work/works/"


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
        charmark = characterblocks[curspot].contents[1].string
        curspot += 1
        charauthorblock = characterblocks[curspot].string
        if len(charauthorblock) > 4:  # we have an author
            charauthor = charauthorblock[4::]
        else:
            charauthor = ""
        curspot += 1
        charworkblock = characterblocks[curspot].string
        if len(charworkblock) > 3:
            workauthor = charworkblock[3::]
        else:
            workauthor = ""
        curspot += 1
        characterblocks[curspot].unwrap()
        filepathname = characterblocks[curspot].attrs['id']
        foldername = filepathname[:8]
        pagename = filepathname[19:26]
        filename = filepathname[18:]
        curspot += 1
        charimagefile = open(ROOTDIR + CHARDIR + foldername + "/" + filename, "rb")
        charimage = charimagefile.read()
        character = [charmark, charauthor, workauthor, foldername, pagename, filename, charimage]
        charimagefile.close()
        characters.append(character)
    return characters,

# charpage: [ character, author, work, work_id, page_id, fileName, Binary JPEG ]


def buildpagefromfile(htmlfile):
    charpage = grabcharsfromfile(htmlfile)
    for char in charpage:
        for part in char:
            print(part)


for curfile in range(1, 2):  #5500
    filename = ROOTDIR + HTMDIR + str(curfile) + ".html"
    buildpagefromfile(filename)


