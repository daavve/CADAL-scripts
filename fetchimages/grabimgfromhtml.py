# !/bin/python
#
#
#
#####################################

from bs4 import BeautifulSoup as BS
from pathlib import Path
import os

BASEPATH="www.cadal.zju.edu.cn/CalliSources/books"


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

for childdir in os.listdir(BASEPATH):
    childpath = os.path.join(BASEPATH, childdir)
    fullchildpath = os.path.join(childpath, "otiff")
    infile = open(os.path.join(fullchildpath, "index.html"), mode='r')
    htmlfile = infile.read()
    infile.close()
    outfile = open(os.path.join(fullchildpath, "downloadlist.txt"), mode="w")
    filenames = runbs(htmlfile)
    for file in filenames:
        outfile.write("http://" + str(fullchildpath) + "/" + file + "\n")
    outfile.close()


