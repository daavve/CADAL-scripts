#! /bin/python
#
#   Builds a tree compatable with Django Database
#   Note, composite itterator method would make this clearer, probably.  But not doing it.
#
##########################################


import json


class Charjson(object):
    def __init__(self, mark: str, author: str, work: str, work_id: str, page_id: str, coordinates: [str]):
        self.chi_mark = mark
        self.chi_author = author
        self.chi_work = work
        self.work_id = work_id
        self.page_id = page_id
        self.xy_coordinates = coordinates


class Book(object):
    def __init__(self, bid: int, title: str, author: str):
        self.bid = bid
        self.title = title
        self.author = author
        self.pages = [Page]

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


class Page(object):
    def __init__(self, number: int):
        self.number = number
        self.characters = [Character]

    def addchar(self, n: Charjson) -> None:
        self.characters.append(Character(n.chi_mark, int(n.xy_coordinates[0]),
                                                     int(n.xy_coordinates[1]),
                                                     int(n.xy_coordinates[2]),
                                                     int(n.xy_coordinates[3])))

class Character(object):
    def __init__(self, mark: str, x1: int, y1: int, x2: int, y2: int):
        self.mark = mark
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

books = [Book]


def addnewbook(newchar: Charjson) -> None:
    newbook = Book(int(newchar.work_id), newchar.chi_work, newchar.chi_author)
    newbook.addchar(newchar)
    books.append(newbook)


def inserttobook(newchar: Charjson) -> None:
    if len(books) >= 1:
        foundbook = False
        for book in books:
            if book.id == int(newchar.work_id):
                book.addchar(newchar)
                foundbook = True
                break
        if not foundbook:
            addnewbook(newchar)
    else:
        addnewbook(newchar)


def readjson(filename: str) -> [Charjson]:  # Not too bad, less than 70M
    jsonfile = open(filename, "r")
    readfile = json.load(jsonfile)
    jsonfile.close()
    characters = [Charjson]
    for r in readfile:
        characters.append(
            Charjson(r['chi_mark'], r['chi_author'], r['chi_work'], r['work_id'], r['page_id'], r['xy_coordinates']))
    return characters


chars = readjson("dump.json")
for char in chars:
    inserttobook(char)
