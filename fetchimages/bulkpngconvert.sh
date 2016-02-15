#!/usr/bin/env bash
#
# Converts tiff images to png's
#
##########################################

cd "www.cadal.zju.edu.cn/CalliSources/books"
START_DIR=$(pwd)
for i in $(find . -maxdepth 1 -type d); do
    if [ ${i:3} ]; then
        cd ${i:2}"/otiff"
        for j in $(ls *.tif); do
            echo $j
            convert -quality 9 $j {j:0:8}".png"
            rm $i
        done
        cd $START_DIR
    fi
done
