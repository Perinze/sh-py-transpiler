#!/usr/bin/python3 -u
import os

if os.path.exists('/dev/null'):
    print('e')


if os.path.isfile('/dev/null'):
    print('f')


if os.path.isdir('/dev/null'):
    print('d')


if os.path.isdir('/dev'):
    print('d')

