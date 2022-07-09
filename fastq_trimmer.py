#!/usr/bin/python3

import sys

args = sys.argv
middle = False
files = ""
if len(args) == 1 or args[1] == "-h" or args[1] == "--help":
    print("""Help menu:
Mandatory flags:
    -i  destination to the input file (single or multi fastq files)
Optional flags:
    -m  if chosen, middle bases under threshold will be replaced with '-' (default false)
    -t  threshold (default 20)""")
    sys.exit()

if "-i" in args:
    for i in args[args.index("-i") + 1:]:
        if i.startswith("-"):
            ind = args.index(i)
            files = args[args.index("-i") +1:ind]
    if files == "":
        files = args[args.index("-i")+1:]
else:
    print("-i is mandatory")
    sys.exit()

if "-t" in args:
    threshold = int(args[args.index("-t") + 1])
else:
    threshold = 20

if "-m" in sys.argv:
    middle = True

def qual(x):
    return ord(x) - 33

for file in files:
    with open(file) as f:
    	count = sum(1 for line in f)//4
    with open(file) as f:
        for i in range(count):
            meta = f.readline()[:-1]
            seq = f.readline()
            f.readline()
            q = list(f.readline()[:-1])
            b, e = 0, 0
            
            ln = len(q)

            for j in range(0, ln, 3):
                if sum(map(qual, q[j:j+3]))/3 >= threshold:
                    b = j
                    break
            for j in range(ln-3, -1, -3):
                if sum(map(qual, q[j:j+3]))/3 >= threshold:
                    e = j+3
                    break
            q = q[b:e]
            
            if middle:
                for j in range(0, len(q)//3+1, 3):
                    if sum(map(qual, q[j:j+3]))/3 < threshold:
                        q[j:j+3] = ["-", "-", "-"]
            q = "".join(q)
            print(meta)
            print(seq[b:e])
            print("+")
            print(q)

