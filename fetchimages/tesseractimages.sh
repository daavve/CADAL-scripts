#!/usr/bin/env bash
#
# Runs Tesseract on downloaded images
#
####################################

cd "www.cadal.zju.edu.cn/CalliSources/booksserve"
START_DIR=$(pwd)
for i in $(find . -type d -maxdepth 1); do
    if [ ${i:3} ]; then
        cd ${i:2}"/otiff"
        if [ -e 00000001.tif ]; then
            for j in $(ls *.tif); do
                tesseract $j -l chi_tra stdout | tee ${j:0:8}".txt"
            done
        else
            for j in $(ls *.jpg); do
                tesseract $j -l chi_tra stdout | tee ${j:0:8}".txt"
            done
        fi

        cd $START_DIR
    fi
done
