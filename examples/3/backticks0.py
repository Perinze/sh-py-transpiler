#!/usr/bin/python3 -u
import subprocess
a = subprocess.run(['printf', 'hi'], text=True, stdout=subprocess.PIPE).stdout.strip()
print(a)
