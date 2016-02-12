# !/bin/python
#
#
#
#####################################

from bs4 import BeautifulSoup as BS
from urllib import request
from pathlib import Path
import os

BASEPATH="www.cadal.zju.edu.cn/CalliSources/books"


def runbs(inhtml: str) -> [str]:
    soup = BS(inhtml, "html.parser")
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
    infile = open(os.path.join(fullchildpath, "index.html"), 'r')
    htmlfile = infile.read()
    infile.close()
    filenames = runbs(htmlfile)
    for file in filenames:
        fullpath = Path(os.path.join(fullchildpath, file))
        webpath = "http://" + str(fullpath)
        webfile = request.urlopen(webpath)
        webimage = webfile.read()
        webfile.close()
        fullpath.write_bytes(webimage)