#!/usr/bin/env bash
#
# mass wget from CADAL Website
#
#
####################################################

for cur in `seq 1 10000`; do
    wget http://www.cadal.zju.edu.cn/NewCalligraphy/worklist.jsp?page_id=$cur
done
