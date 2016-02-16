#!/usr/bin/env bash
#
# Runs Tesseract on downloaded images
#
####################################

cd "www.cadal.zju.edu.cn/CalliSources/books_local"
START_DIR=$(pwd)
for i in $(find . -maxdepth 1 -type d); do
    if [ ${i:3} ]; then
        cd ${i:2}"/otiff"
        for j in $(ls *.jpg); do
            echo $j
            if [ ! -f ${j:0:8}".txt" ]; then
                tesseract $j -l chi_tra stdout | tee ${j:0:8}".txt"
            fi
        done
        cd $START_DIR
    fi
done
