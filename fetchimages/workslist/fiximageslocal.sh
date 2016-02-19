#!/usr/bin/env bash
#
# Use the list we got server-side to fix local tif .jpg to tif.tif
#
###############################################################

BOOK_BASE="/home/dave/workspace/pycharm/CADAL-scripts/fetchimages/workslist/grabbedBooks"

booklist=$(cat "/home/dave/workspace/pycharm/CADAL-scripts/fetchimages/workslist/grabbedBooks/tiffbooks.txt")


cd $BOOK_BASE
for book in $booklist; do
    bookjpg=${book:0:17}".jpg"
    mv $bookjpg $bookjpg
done