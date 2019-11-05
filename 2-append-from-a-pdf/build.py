#!/usr/bin/env python3

import re


entryPattern = re.compile("^[A-Z]([0-9\\.\\-]+)?\s.+")
isEntry = lambda i: entryPattern.match(i.strip())

raw = []

for line in open("original.txt", "r"):
    if isEntry(line): raw.append(line.strip())

for line in open("source.txt", "r"):
    if isEntry(line): raw.append(line.strip())

raw = list(set(raw))
raw.sort()

"""for i in range(0, len(raw)):
    s = raw[i].find(" ")
    raw[i] = raw[i][:s], raw[i][s+1:]"""

tree = {}         # ID => mother ID
catalogNames = {} # ID => name
for i in range(0, len(raw)):
    s = raw[i].find(" ")
    tree[raw[i][:s]] = "" 
    catalogNames[raw[i][:s]] = raw[i][s+1:]

# find the direct mother of a catalog

for leaf in tree:
    catalog = leaf
    while catalog != "":
        catalog = catalog[:-1]
        if catalog in catalogNames: break
    tree[leaf] = catalog


def printtree(catalog):
    
    parentlevel = (catalog == "")
    if not parentlevel:
        yield catalog + " " + catalogNames[catalog]

    for leaf in tree:
        if tree[leaf] == catalog:
            for childleaf in printtree(leaf):
                yield ("\t" if not parentlevel else "") + childleaf

for line in printtree(""):
    print(line)
