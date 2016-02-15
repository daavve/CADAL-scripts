#!/usr/bin/env bash
#
# Converts tiff images to png's
#
##########################################

cd "www.cadal.zju.edu.cn/CalliSources/books_local"
START_DIR=$(pwd)
for i in $(find . -maxdepth 1 -type d); do
    if [ ${i:3} ]; then
        cd ${i:2}"/otiff"
        for j in $(ls *.tif); do
            jid=$(identify $j | grep '8-bit')
            if [ ${jid:3} ]; then
                convert -verbose -quality 9 $j ${j:0:8}".png"

            else
                convert -verbose -quality 9 -colors 4 $j ${j:0:8}".png"
            fi
            rm $j
        done
        cd $START_DIR
    fi
done
