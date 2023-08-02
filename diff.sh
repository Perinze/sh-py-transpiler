#!/bin/bash
for i in 0 1 2
do
    diff $i.log $i.ans
done