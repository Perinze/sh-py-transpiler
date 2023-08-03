#!/usr/bin/python3 -u
import os

if os.access('/dev/null', os.R_OK):
    print('r')


if os.access('/dev/null', os.W_OK):
    print('w')


if os.access('/dev/null', os.X_OK):
    print('x')

