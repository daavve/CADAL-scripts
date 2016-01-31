#! /bin/python
#
#   Builds a tree compatable with Django Database
#   Note, pretty slow and ineficient, as we build use dfs to build character tree.
#
##########################################


import json, os


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


class Page(object):
    def __init__(self, number: int):
        self.number = number
        self.characters = []

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




def buildnewbook(newchar: Charjson) -> Book:
    newbook = Book(int(newchar.work_id), newchar.chi_work, newchar.chi_author)
    newbook.addchar(newchar)
    return newbook


def inserttobook(newchar: Charjson, boks: [Book]) -> None:
    if len(boks) >= 1:
        foundbook = False
        for book in boks:
            if book.bid == int(newchar.work_id):
                book.addchar(newchar)
                foundbook = True
                break
        if not foundbook:
            boks.append(buildnewbook(newchar))
    else:
        boks.append(buildnewbook(newchar))


def readjson(filename: str) -> [Charjson]:  # Not too bad, less than 70M
    jsonfile = open(filename, "r")
    readfile = json.load(jsonfile)
    jsonfile.close()
    characters = []
    for r in readfile:
        characters.append(
            Charjson(r['chi_mark'], r['chi_author'], r['chi_work'], r['work_id'], r['page_id'], r['xy_coordinates']))
    return characters

books = []
chars = readjson("dump.json")
for char in chars:
    inserttobook(char, books)


