#!/usr/bin/env bash
#
# Runs Tesseract on downloaded images
#
####################################

cd "www.cadal.zju.edu.cn/CalliSources/booksserve"
START_DIR=$(pwd)
for i in $(find . -type d -maxdepth 1)
do
    if [ ${i:3} ]; then
        cd ${i:2}"/otiff"
        pwd
        cd $START_DIR
    fi
done
