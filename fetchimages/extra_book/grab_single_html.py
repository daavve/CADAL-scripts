# !/bin/python
#
#
#
#####################################

from bs4 import BeautifulSoup as BS
from pathlib import Path
import os

BASEPATH="www.cadal.zju.edu.cn/CalliSources/books/06100013/otiff/"


def runbs(inhtml: str) -> [str]:
    soup = BS(inhtml, "html5lib") #HTML5 does not break during find_all on big sets
    asoup = soup.find_all('a')
    filenames = []
    skippedfirst = False
    for bsoup in asoup:
        if skippedfirst:
            filenames.append(str(bsoup).split('/')[5].split("\"")[0]) #Probably better to user REGEX here.....
        else:
            skippedfirst = True
    return filenames


infile = open("index.html", mode='r')
htmlfile = infile.read()
infile.close()
outfile = open("downloadlist.txt", mode="w")
filenames = runbs(htmlfile)
for file in filenames:
    outfile.write("http://" + BASEPATH + file + "\n")
outfile.close()


