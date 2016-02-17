#!/usr/bin/env bash
#
# Fetches HTML for works list
#
#######################################################################


for cur in `seq 1 10000`; do
    wget http://www.cadal.zju.edu.cn/NewCalligraphy/workdetail.jsp?contentid=$cur &> /dev/null
done
