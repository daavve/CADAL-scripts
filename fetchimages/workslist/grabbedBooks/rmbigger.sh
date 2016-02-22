#!/usr/bin/env bash
#
# Walks through the .png files, and deletes the smaller one
#
####################################################

declare -i lenT
pnglist=$(ls *.png)

for pngfile in $pnglist; do
    let lenT=${#pngfile}-4
    tiffile=${pngfile:0:$lenT}".png"
    tifSize=$(stat -c %s $tifFile)
    pngSize=$(stat -c %s $pngFile)
    if [[ $tifSize > $pngSize ]]; then
        rm -f $tifFile
    else
        rm -f $pngFile
    fi
done
