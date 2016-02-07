#! /bin/bash
#
#   Run Tesseract ocr on a bunch of images
#
#########################################



for cur in `seq 1 51`; do
    echo ${cur}t.png
    tesseract ${cur}t.png -l chi_tra
    echo "-----------------------"
done
