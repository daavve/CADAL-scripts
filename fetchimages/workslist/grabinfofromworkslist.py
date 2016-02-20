#
# Walks through workdetail html
# Important:  Many books are a collection of works
# The text is very inconsistant sometimes good, sometimes not there
# probably best to just get a blob of text
#
#####################################################################################

from bs4 import BeautifulSoup as BS
import socket
from subprocess import check_output
from subprocess import CalledProcessError
import sys, json, os
from pathlib import Path

if socket.gethostname() == "bigArch":
    BASE_NAME = "/home/dave/workspace/pycharm/fetch/workslist/"
    IMAGE_DIR = "/home/dave/workspace/pycharm/fetch/bookjpeg/"
else:
    BASE_NAME = "/home/django/CADAL-scripts/fetchimages/workslist/"
    IMAGE_DIR = "/home/django/CADAL-scripts/fetchimages/workslist/grabbedBooks/"


WHITESPACE = " 　\u3000"


class Author(object):
    def __init__(self, name: str, dynesty: str):
        self.name = name
        self.dynesty = dynesty
        self.works = []


class Page(object):
    def __init__(self, book_id: str, page_files: [str]):
        self.book_id = book_id
        self.pages_id = page_files


class Collection(object):
    def __init__(self, work_id: int, text_block: str, pages: Page):
        self.work_id = work_id
        self.pages = pages
        self.text_block = text_block

authors = []


def parsehtml(inhtml: str, id_number: int) -> None:
    soup = BS(inhtml, "html5lib")
    soupi = soup.find_all('img')
    soup8 = str(soupi[8]).split('/')
    bookid = soup8[6]
    pages = []
    pages.append(soup8[7].strip('\"'))
    for i in range(10, len(soupi)):
        pages.append(str(soupi[i]).split('/')[7].strip('\"'))
    soupgrab = str(soup.find(id="work_text")).split('\n')
    textblock = ""
    for i in range(1, len(soupgrab) - 1):   #Start and end are HTML
        textblock += soupgrab[i].strip(WHITESPACE) + "\n"
    soup_info = soup.find_all(id="calligrapher_info")
    strstr = str(soup_info).split("name=")[1]
    calligrapher = strstr.split("\"")[0]
    dynesty = strstr.split(',')[1].strip(WHITESPACE)

    newauthor = True
    for author in authors:
        if author.name == calligrapher:
            newauthor = False
            myauthor = author

    if(newauthor):
        myauthor = Author(calligrapher, dynesty)
        authors.append(myauthor)

    myauthor.works.append(Collection(id_number, textblock, Page(bookid, pages)))


def jdefault(o):    # This part is necessary to get the objects to Auto-Format
    return o.__dict__

def dumptojson() -> None:
    dumpfile = open('dump2.json', mode='w')
    json.dump(authors, dumpfile, ensure_ascii=False, indent=4, sort_keys=True, default=jdefault)
    dumpfile.close()

def parsehtml() -> None:
    basepath = Path(BASE_NAME)
    files = basepath.glob('workdetail.jsp?contentid=*')
    for file in files:
        id_number = int(str(file).split('=')[1])
        infile = file.open(mode='r', encoding='utf-8')
        inred = infile.read()
        parsehtml(inred, id_number)
        infile.close()

def readfromjson() -> None:
    jsonfile = open("dump2.json", mode="r", encoding='utf-8')
    readfile = json.load(jsonfile)
    jsonfile.close()
    for r in readfile:
        x=1
        author1 = Author(r['name'], r['dynesty'])
        for w in r['works']:
            author1.works.append(Collection(w['work_id'],
                                            w['text_block'],
                                            Page(w['pages']['book_id'],
                                                 w['pages']['pages_id'])))
        authors.append(author1)

#parsehtml()
#dumptojson()
readfromjson()

WEBSITE = "http://www.cadal.zju.edu.cn/CalliSources/books/"
WEBBACKUP = "http://www.cadal.zju.edu.cn/CalliSources/images/books/"

failedwork = []

author_num = 0
for author in authors:
    author_num += 1
    for work in author.works:
        workid = work.work_id
        pages = work.pages
        bookid = pages.book_id
        for page in pages.pages_id:
            webstringjpeg = WEBSITE + bookid + '/otiff/' + page
            webstringtiff = webstringjpeg[:len(webstringjpeg) - 3] + "tif"
            webback = WEBBACKUP + bookid + '/' + page
            outfilestringjpg = IMAGE_DIR + bookid + '-' + page
            outfilestringtif = outfilestringjpg[:len(outfilestringjpg) - 3] + "tif"
            if not os.path.isfile(outfilestringjpg) and not os.path.isfile(outfilestringtif):
                try:
                    check_output(['wget', webstringtiff, '-O', outfilestringtif])
                except CalledProcessError:
                    try:
                        check_output(['wget', webstringjpeg, '-O', outfilestringjpg])
                    except CalledProcessError:
                        try:
                            check_output(['wget', webback, '-O', outfilestringjpg])
                        except CalledProcessError:
                            failedwork.append(workid + ":" + bookid + ":" + page)
print("-------FAILED------------")
for faild in failedwork:
    print(faild)


