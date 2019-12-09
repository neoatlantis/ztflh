#!/usr/bin/env python3
import os
import re
import json
from logging import *

ALL_CLASSIFICATIONS = {}
ALL_CLASSIFICATIONS_JSON = None
CACHE_FILE = os.path.join(os.path.dirname(__file__), "classification.json")

def generateClassificationCache():
    global ALL_CLASSIFICATIONS
    global ALL_CLASSIFICATIONS_JSON

    _csource = [e.rstrip() for e in open(
            os.path.join(os.path.dirname(__file__), "classification.txt")
        ).read().split("\n") if e.strip()]

    def splitentry(line):
        x = line.find(" ")
        return line[:x].strip(), line[x:].strip()

    CLASSIFICATIONS_BY_LEVEL = {}

    for level in range(0, 5):
        CLASSIFICATIONS_BY_LEVEL[level] = {}

        searcher = re.compile("^\\t{%d}[^\\t]+$" % level)
        for line in _csource:
            if searcher.match(line):
                cid, cname = splitentry(line)
                CLASSIFICATIONS_BY_LEVEL[level][cid] = cname

    for level in CLASSIFICATIONS_BY_LEVEL:
        for cid in CLASSIFICATIONS_BY_LEVEL[level]:
            cname = CLASSIFICATIONS_BY_LEVEL[level][cid]
            ALL_CLASSIFICATIONS[cid] = [cname, level, None]
            #{ "n": cname, "l": level, "p": None}

    for cid in ALL_CLASSIFICATIONS:
        level = ALL_CLASSIFICATIONS[cid][1]
        if level > 0:
            plevel = level - 1
            found = False
            for pcid in CLASSIFICATIONS_BY_LEVEL[plevel]:
                if cid.startswith(pcid):
                    ALL_CLASSIFICATIONS[cid][2] = pcid
                    found = True
                    break

    ALL_CLASSIFICATIONS_JSON = json.dumps(ALL_CLASSIFICATIONS, ensure_ascii=False)
    open(CACHE_FILE, "w+").write(ALL_CLASSIFICATIONS_JSON)

def getClassificationHierachy(c):
    global ALL_CLASSIFICATIONS
    while c and  c not in ALL_CLASSIFICATIONS:
        c = c[:-1]
    if not c: return None
    ret = [ALL_CLASSIFICATIONS[c]]
    while ret[0]["p"] is not None:
        ret.insert(0, ALL_CLASSIFICATIONS[ret[0]["p"]])
    ret = [(e["l"], e["n"]) for e in ret]
    return ret



if os.path.isfile(CACHE_FILE):
    ALL_CLASSIFICATIONS_JSON = open(CACHE_FILE, "r").read()
    ALL_CLASSIFICATIONS = json.loads(ALL_CLASSIFICATIONS_JSON)
    info("Loaded classification data from cache.")
    info("To reload classification data, remove cache file <%s>." % CACHE_FILE)
else:
    warn("Classification cache not found. Generate one for you.")
    warn("If error arises, check permission for cache file directory.")
    generateClassificationCache()

open("classification.js", "w").write(
    "const CLASSIFICATIONS=%s;" % ALL_CLASSIFICATIONS_JSON)
