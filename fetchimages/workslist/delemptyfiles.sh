#!/usr/bin/env bash
#
# Find all file types of "empty" and delete them
#
##################################

BASE_DIR="/home/dave/workspace/pycharm/fetch/grabbedBooks/"

declare -i offset
let offset=${#BASE_DIR}+23
for file in $(ls $BASE_DIR); do
    fileloc=$BASE_DIR$file
    filetype=$(file $fileloc)
    if [[ ${filetype:$offset:5} == "empty" ]]; then
        echo "DELETE: "$file
    fi
done
