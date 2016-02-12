#! /bin/bash
#
# Batch renaming to fix mislabeled files
#
###############################################


for cur in 'seq 1 50'; do
    mv ${cur}t_v1.png ${cur}t.png
