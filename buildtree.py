#! /bin/python
#
#   Builds a tree compatable with Django Database
#
##########################################

from typing import List

class Characterfull(object):
    def __init__(self, mark: str, author: str, work: str, work_id: str, page_id: str, coordinates: List[str]):
        self.chi_mark = mark
        self.chi_author = author
        self.chi_work = work
        self.work_id = work_id
        self.page_id = page_id
        self.xy_coordinates = coordinates


class Book(object):
    def __init__(self, id: int, title: str, author: str, source: str):
        self.id = id
        self.title = title
        self.author = author
        self.source = source
        self.pages = List[Page]


class Page(object):
    def __init__(self, number: int):
        self.number = number
        self.characters = List[Character]


class Character(object):
    def __init__(self, mark: str, x1: int, y1: int, x2: int, y2: int):
        self.mark = mark
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2





