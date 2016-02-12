#!/usr/bin/env bash
#
#   Grabs appropriate images from CADAL
#
############################



BASEWEB="http://www.cadal.zju.edu.cn/CalliSources/books/"

DIRLIST=$(cat dirlist.txt)

for dir in $DIRLIST; do
    echo "Grabbing: " $dir
    wget -m --no-parent -r $BASEWEB"/"$dir"/otiff/"
done