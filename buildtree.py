#! /bin/python
#
#   Builds a tree compatable with Django Database
#   Note, pretty slow and ineficient.
#   The items in the nodes get walked though.  A search would be much more efficient.
#
##########################################


import json, os, stat


class Charjson(object):
    def __init__(self, mark: str, author: str, work: str, work_id: str, page_id: str, coordinates: [str]):
        self.chi_mark = mark
        self.chi_author = author
        self.chi_work = work
        self.work_id = work_id
        self.page_id = page_id
        self.xy_coordinates = coordinates


class Library(object):
    def __init__(self, title: str):
        self.title = title
        self.collections = []


class Collection(object):
    def __init__(self, title: str):
        self.title = title
        self.books = []

    def addnewbook(self,newchar: Charjson) -> None:
        newbook = Book(int(newchar.work_id), newchar.chi_work, newchar.chi_author)
        newbook.addchar(newchar)
        self.books.append(newbook)

    def addchar(self, newchar: Charjson) -> None:
        if len(self.books) >= 1:
            foundbook = False
            for book in self.books:
                if book.bid == int(newchar.work_id):
                    book.addchar(newchar)
                    foundbook = True
                    break
            if not foundbook:
                self.addnewbook(newchar)
        else:
            self.addnewbook(newchar)

    def addpagetobook(self, newpage: Charjson) -> None:
        newbook = Book(int(newpage.work_id), newpage.chi_work, newpage.chi_author)
        newbook.addpage(newpage)
        self.books.append(newbook)

    def addpage(self, newpage: Charjson) -> None:
        if len(self.books ) >= 1:
            for book in self.books:
                foundbook = False
                if book.bid == int(newpage.work_id):
                    book.addPage(newpage)
                    foundbook = True
                    break
                if not foundbook:
                    self.addpagetobook(newpage)
        else:
            self.addpagetobook(newpage)

class Book(object):
    def __init__(self, bid: int, title: str, author: str):
        self.bid = bid
        self.title = title
        self.author = author
        self.pages = []

    def addnewpage(self, newchar: Charjson) -> None:
        newpage = Page(int(newchar.page_id))
        newpage.addchar(newchar)
        self.pages.append(newpage)

    def addchar(self, newchar: Charjson) -> None:
        if len(self.pages) >= 1:
            foundpage = False
            for page in self.pages:
                if page.number == int(newchar.page_id):
                    foundpage = True
                    page.addchar(newchar)
                    break
            if not foundpage:
                self.addnewpage(newchar)
        else:
            self.addnewpage(newchar)


    def addpage(self, newpage: Charjson) -> None:
        if len(self.pages) >= 1:
            foundpage = False
            for page in self.pages:
                if page.number == int(newpage.page_id):
                    foundpage = True
                    break
            if not foundpage:
                self.pages.append(Page(int(newpage.page_id)))
        else:
            self.pages.append(Page(int(newpage.page_id)))





class Page(object):
    def __init__(self, number: int):
        self.number = number
        self.characters = []

    def addnewchar(self, newchar: Charjson) -> None:
        self.characters.append(Character(newchar.chi_mark, int(newchar.xy_coordinates[0]),
                                                     int(newchar.xy_coordinates[1]),
                                                     int(newchar.xy_coordinates[2]),
                                                     int(newchar.xy_coordinates[3])))

    def addchar(self, newchar: Charjson) -> None:
        if len(self.characters) >= 1:
            foundchar = False
            for chara in self.characters:
                if int(newchar.xy_coordinates[0]) == chara.x1 and int(newchar.xy_coordinates[1]) == chara.y1 and int(newchar.xy_coordinates[2]) == chara.x2 and int(newchar.xy_coordinates[3]) == chara.y2:
                    foundchar = True
                    break
            if not foundchar:
                self.addnewchar(newchar)
        else:
            self.addnewchar(newchar)


class Character(object):
    def __init__(self, mark: str, x1: int, y1: int, x2: int, y2: int):
        self.mark = mark
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2


def readjson(filename: str) -> [Charjson]:  # Not too bad, less than 70M
    jsonfile = open(filename, "r")
    readfile = json.load(jsonfile)
    jsonfile.close()
    characters = []
    for r in readfile:
        characters.append(
            Charjson(r['chi_mark'], r['chi_author'], r['chi_work'], r['work_id'], r['page_id'], r['xy_coordinates']))
    return characters

ROOTDIR = "fetch/"
HTMDIR = "charDataHTML/"
BOOKSDIR = "CalliSources/books/"
CHARDIR = "cadal/characterimage/"


def getcharsbyfilename() -> [Charjson]:
    charfiles = []
    for f in os.listdir(ROOTDIR + CHARDIR):
        pathname = os.path.join(ROOTDIR + CHARDIR, f)
        booknum = str(pathname).split('/')[3]
        if stat.S_ISDIR(os.stat(pathname).st_mode):
            for img in os.listdir(pathname):
                if img.endswith('.jpg'):
                    imgs = img.split('(')
                    pagenum = imgs[0]
                    coords = imgs[1].strip(').jpg').split(',')
                    charfiles.append(Charjson("Page", "?", "?",booknum, pagenum, coords))
    return charfiles


def loadimagelist() -> [Charjson]:  # I know cut / paste coding is bad, but i'm in a hurry
    imgfiles = []
    for f in os.listdir(ROOTDIR + BOOKSDIR):
        pathname = os.path.join(ROOTDIR + BOOKSDIR, f)
        booknum = str(pathname).split('/')[3]
        if stat.S_ISDIR(os.stat(pathname).st_mode):
            for img in os.listdir(pathname):
                if img.endswith('.jpg'):
                    imgname = img.strip('.jpg')
                    imgfiles.append(Charjson("?", "?", "?", booknum, imgname, [0, 0, 0, 0]))
    return imgfiles

library = Library("Calligraphy")
library.collections.append(Collection("CADAL"))
library.collections.append(Collection("KOSUKE"))
chars = readjson('dump.json')
for char in chars:
    library.collections[0].addchar(char)

filechars = getcharsbyfilename()
for char in filechars:
    library.collections[0].addchar(char)

pageonly = loadimagelist()
for page in pageonly:
    library.collections[0].addpage(page)


input("press anykey -->")
