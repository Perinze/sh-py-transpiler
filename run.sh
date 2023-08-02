#!/bin/bash
for i in 0 1 2
do
    echo > $i.log
    for f in `ls examples/$i/*.sh`
    do
        ./sheepy.py $f >> $i.log
    done
done