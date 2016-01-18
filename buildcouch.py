#! /bin/python
#
#   Grabs characters from JSON file and imports them into couchDB
#
##########################################
from couchdb import client
from couchdb.mapping import Document, DictField, TextField, IntegerField, Mapping
import json


class Character(Document):
    ch_character =  TextField()
    ch_author =     TextField()
    ch_work =       TextField()
    id_work =       IntegerField()
    id_page =       IntegerField()
    id_xypos =      DictField(Mapping.build(
        coord_x1 =  IntegerField(),
        coord_y1 =  IntegerField(),
        coord_x2 =  IntegerField(),
        coord_y2 =  IntegerField()
    ))


def builddbfromjsonfile() -> None:
    jsonfile = open("dump.json", "r")
    readfile = json.load(jsonfile)
    jsonfile.close()
    srvr = client.Server()
    db = srvr.create('characters')
    for r in readfile:
        character = Character(ch_character=r['chi_mark'],
                              ch_author=   r['chi_author'],
                              ch_work=     r['chi_work'],
                              id_work=     r['work_id'],
                              id_page=     r['page_id'],
                              id_xypos=dict(coord_x1=r['xy_coordinates'][0],
                              coord_y1=r['xy_coordinates'][1],
                              coord_x2=r['xy_coordinates'][2],
                              coord_y2=r['xy_coordinates'][3]))
        character.store(db)


builddbfromjsonfile()
