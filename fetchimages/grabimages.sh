#!/usr/bin/env bash
#
#   Grabs appropriate images from CADAL
#
############################


filelist=$(find www.cadal.zju.edu.cn/ -name "downloadlist.txt")

for file in $filelist; do
    filedir=${file::55}
    weblist=$(cat $file)
    for web in $weblist; do
        outfile=$filedir${web:62}
        wget --output-document=$outfile $web
    done
done



