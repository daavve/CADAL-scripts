#!/usr/bin/env bash
#
# Fetches the translation page of each book from CADAL website
#
########################################################

declare -i count

let count=0

webbaddr="http://www.cadal.zju.edu.cn/NewCalligraphy/workdetail.jsp?contentid="

while [ $count -le 80 ]; do
    curl ${webbaddr}${count} -o translate-${count}.html
    let count=count+1
done