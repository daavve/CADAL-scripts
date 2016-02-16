#!/usr/bin/env bash
#
#   Grabs appropriate images from CADAL
#
############################


weblist=$(cat "downloadlist.txt")
for web in $weblist; do
    outfile=$filedir${web:62}
    if [ ! -e $outfile ]; then
        wget --output-document=$outfile $web
    fi
done



