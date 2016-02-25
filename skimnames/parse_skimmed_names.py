#
#  extracts relevant information from skimmed html files
#
#####################################################################

import os
import socket
import json
from bs4 import BeautifulSoup as BS
from bs4.element import Tag

if socket.gethostname() == 'bigArch':
    SKIMM_FOLDER = "/home/dave/workspace/pycharm/fetch/skimmedWorklist/"
else:
    SKIMM_FOLDER = "/media/skimmedWorklist"

END_STRING = "\n                                "

class Workinfo(object):
    def __init__(self, wkid: str, wktitle: str, wkauthor: str):
        self.wkid = wkid
        self.wktitle = wktitle
        self.wkauthor = wkauthor

wrks = []


def extractinfo(info: Tag) -> None:
    if info is not None:
        workid = str(info['href']).split('=')[1]
        ps = info.find_all('p')
        worktitle = str(ps[0]).strip('<p>/')
        workauthor = str(ps[1]).strip('<p>/')
        wrks.append(Workinfo(workid, worktitle, workauthor))



def parsefile(inhtml: str) -> None:
    soup = BS(inhtml, "html5lib")
    seg = soup.tr
    while str(seg) != END_STRING:
        for desc in seg.children:
            extractinfo(desc.a)
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


def jdefault(o):    # This part is necessary to get the objects to Auto-Format
    return o.__dict__

def dumptojson() -> None:
    dumpfile = open('wrk-titles.json', mode='w')
    json.dump(wrks, dumpfile, ensure_ascii=False, indent=4, sort_keys=True, default=jdefault)
    dumpfile.close()



htmlfiles = find_html_files(SKIMM_FOLDER)
for htmlfile in htmlfiles:
    file = open(htmlfile, mode='r', encoding='utf-8')
    filehtml = file.read()
    file.close()
    parsefile(filehtml)
dumptojson()
