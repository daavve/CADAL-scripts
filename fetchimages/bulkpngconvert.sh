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
        for tiffile in $(ls *.tif); do
            pngfile=${tiffile:0:8}".png"
            convert -verbose -quality 9 $tiffile $pngfile # Sometimes png is bigger than tif.
            sizetiff=$(du -k "$tiffile" | cut -f 1)
            sizepng=$(du -k "$pngfile" | cut -f 1)
            if [ $sizetiff -lt $sizepng ]; then
                rm $pngfile
            else
                rm $tiffile
            fi
        done
        cd $START_DIR
    fi
done
