#!/usr/bin/env bash
#
# Converts tiff images to png's
#
##########################################

declare -i length

cd "www.cadal.zju.edu.cn/CalliSources/books"
START_DIR=$(pwd)
for i in $(find . -maxdepth 1 -type d); do
    if [ ${i:3} ]; then
        cd ${i:2}"/otiff"
        for j in $(ls *.tif); do
            echo "identify: "$j
            jid=$(identify $j | grep '8-bit') # Binary images get bigger when we compress them?
            length=${#jid}
            if [ length -gt 3 ]; then
                convert -verbose -quality 9 $j ${j:0:8}".png"
                rm $j
            fi
        done
        cd $START_DIR
    fi
done
