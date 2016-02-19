#!/usr/bin/env bash
#
#   Grabs appropriate images from CADAL
#
############################


CHARS_DIR="/home/dave/workspace/pycharm/fetch/chars/"
BOOK_DIR="/home/dave/workspace/pycharm/fetch/grabbedBooks/grabbedBooks/"
WEBSITE="http://www.cadal.zju.edu.cn/CalliSources/books/"
WEBBACKUP="http://www.cadal.zju.edu.cn/CalliSources/images/books/"

cd $CHARS_DIR

for dir in $(ls -d */); do
    for file in $(ls $dir); do
        fileid=${file::8}
        localfile=$BOOK_DIR${dir:0:8}"-"$fileid
        localfilejpg=$localfile".jpg"
        localfiletif=$localfile".tif"
        if [[ -e $localfilejpg || -e $localfiletif ]]; then
            echo "Have: "$localfile
        else
            webbook=$WEBSITE$dir"otiff"$fileid
            webbooktif=$webbook".tif"
            webbookjpg=$webbook".jpg"
            wget $webbooktif -O $localfiletif
            if [[ $? != 0 ]]; then
                wget $webbookjpg -O $localfilejpg
            fi
        fi
    done
done



