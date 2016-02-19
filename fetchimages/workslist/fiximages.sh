#!/usr/bin/env bash
#
# Check all .jpg files to see if they are actually TIFF, rename as appropriate
#
#########################################################

cd "/home/django/CADAL-scripts/fetchimages/workslist/grabbedBooks"

for file in $(ls *.jpg); do
    iden=$(identify $file)
    if [ ${iden:22:4} == "TIFF" ]; then
        mv $file ${file:0:17}".tif"
    fi
done
