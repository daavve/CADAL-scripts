#!/usr/bin/env bash
#
#   Grabs appropriate images from CADAL
#
############################


CHARS_DIR="/home/django/CADAL-scripts/fetchimages/chars"
BOOK_DIR="/home/django/CADAL-scripts/fetchimages/workslist/grabbedBooks/"
WEBSITE="http://www.cadal.zju.edu.cn/CalliSources/books/"
WEBBACKUP="http://www.cadal.zju.edu.cn/CalliSources/images/books/"

emptyfiles=$(cat emptyImages.txt)
for file in $emptyfiles; do
    rm -f $BOOK_DIR$file
done


cd $CHARS_DIR

for dir in $(ls -d */); do
    for file in $(ls $dir); do
        fileid=${file::8}
        localfile=$BOOK_DIR${dir:0:8}"-"$fileid
        localfilejpg=$localfile".jpg"
        localfiletif=$localfile".tif"
        if [[ -e $localfilejpg || -e $localfiletif ]]; then
            x=1
        else
            webbook=$WEBSITE$dir"otiff/"$fileid
            backupsite=$WEBBACKUP$dir$fileid".jpg"
            webbooktif=$webbook".tif"
            webbookjpg=$webbook".jpg"
            wget $webbooktif -O $localfiletif &> /dev/null
            if [[ $? != 0 ]]; then
                rm $localfiletif
                wget $webbookjpg -O $localfilejpg &> /dev/null
                if [[ $? != 0 ]]; then
                    wget $backupsite -O $localfilejpg &> /dev/null
                fi
            fi
        fi
    done
done



