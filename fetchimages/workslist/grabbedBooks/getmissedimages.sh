#!/usr/bin/env bash
#
# Grab Jpegs we somehow missed earlier
#
####################################################


PREFIX="http://www.cadal.zju.edu.cn/CalliSources/images/books/"
fileList=$(cat "missedfiles.txt")
for file in $fileList; do
    webaddr=$PREFIX$file
    outfile=$("$file" | tr '/' '-')
    echo $outfile
done
