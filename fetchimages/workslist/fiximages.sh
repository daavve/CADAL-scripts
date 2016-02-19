#!/usr/bin/env bash
#
# Check all .jpg files to see if they are actually TIFF, rename as appropriate
#
#########################################################

cd "/home/django/CADAL-scripts/fetchimages/workslist/grabbedBooks"

for file in $(ls *.jpg); do
    iden=$(identify $file)
    echo $iden
    if [ ${iden:23:4} == "TIFF" ]; then
        mv $file ${file:17}".tif"
    fi

done