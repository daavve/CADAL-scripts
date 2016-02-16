#!/usr/bin/env bash
#
# Fetches HTML for works list
#
#######################################################################


for cur in `seq 1 80`; do
    wget http://www.cadal.zju.edu.cn/NewCalligraphy/workdetail.jsp?contentid=$cur
done
