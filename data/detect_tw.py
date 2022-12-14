import sys

cn = set()
with open("cntw.mono.tsv") as fo:
    for line in fo:
        s, *t = line.strip().split("\t")
        if s in t:
            continue
        cn.add(s)

for line in sys.stdin:
    if cn.intersection(line):
        continue
    print(line, end = "")
