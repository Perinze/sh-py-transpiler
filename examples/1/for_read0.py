#!/usr/bin/python3 -u
import sys

for n in 'one', 'two', 'three':
    line = sys.stdin.readline().strip()
    print('Line', n, line)
