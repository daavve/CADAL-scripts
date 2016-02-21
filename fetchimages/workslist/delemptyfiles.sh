#!/usr/bin/env bash
#
# Find all file types of "empty" and delete them
#
##################################


if [[ $(hostname) == "bigArch" ]]; then
    BASE_DIR="/home/dave/workspace/pycharm/fetch/grabbedBooks/"
else
    BASE_DIR="/home/django/CADAL-scripts/fetchimages/workslist/grabbedBooks/"
fi

declare -i offset
let offset=${#BASE_DIR}+23
for file in $(ls $BASE_DIR); do
    fileloc=$BASE_DIR$file
    filetype=$(file $fileloc)
    if [[ ${filetype:$offset:5} == "empty" ]]; then
       rm -f $fileloc
    fi
done
