#!/usr/bin/python3 -u
import glob

print(" ".join(sorted(glob.glob("*"))))

C_files = sorted(glob.glob(f"*.[ch]"))
print(f"{' '.join(C_files)}")

