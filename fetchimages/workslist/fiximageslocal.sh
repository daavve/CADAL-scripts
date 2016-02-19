#!/usr/bin/env bash
#
# Use the list we got server-side to fix local tif .jpg to tif.tif
#
###############################################################

BOOK_BASE="/home/dave/workspace/pycharm/fetch/grabbedBooks/grabbedBooks/"

booklist=$(cat "/home/dave/workspace/pycharm/CADAL-scripts/fetchimages/workslist/grabbedBooks/tiffbooks.txt")

for book in $booklist; do
    bookjpg=${book:0:17}".jpg"
    fullbookjpg=$BOOK_BASE$bookjpg
    fullbooktif=$BOOK_BASE$book
    mv $fullbookjpg $fullbooktif
done