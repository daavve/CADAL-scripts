#
#  extracts relevant information from skimmed html files
#
#####################################################################

import os
import socket
from bs4 import BeautifulSoup as BS
from bs4.element import Tag

if socket.gethostname() == 'bigArch':
    SKIMM_FOLDER = "/home/dave/workspace/pycharm/fetch/skimmedWorklist/"
else:
    SKIMM_FOLDER = "/media/skimmedWorklist"

END_STRING = "\n                                "


def extractinfo(info: Tag) -> None:
    x=1


def parsefile(inhtml: str) -> None:
    soup = BS(inhtml, "html5lib")
    seg = soup.tr
    while str(seg) != END_STRING:
        for desc in seg.children:
            extractinfo(desc)
        seg = seg.next_sibling
        x=1
    x=1



def find_html_files(inFolder: str) -> [str]:
    file_list = []
    filename = inFolder + 'worklist.jsp'
    if os.path.isfile(filename):
        file_list.append(filename)
    for x in range(1, 10001):
        filename = inFolder + 'worklist.jsp?page_id=' + str(x)
        if os.path.isfile(filename):
            file_list.append(filename)
    return file_list


htmlfiles = find_html_files(SKIMM_FOLDER)
for htmlfile in htmlfiles:
    file = open(htmlfile, mode='r', encoding='utf-8')
    filehtml = file.read()
    file.close()
    parsefile(filehtml)
