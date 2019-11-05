#!/usr/bin/env python3

import re

pattern1 = ">([A-Z0-9\\.\\-\\+]+)</span>"
pattern2 = "c=([0-9]+).+\">([^<>]+)</a>"
p1search = re.compile(pattern1)
p2search = re.compile(pattern2)


def findInPage(c=None):
    filename = "index.html" + ("@c=%s.html" % c if c is not None else "")
    try:
        source = open("www.ztflh.com/%s" % filename, "r").read()
    except:
        return

    lines = [e for e in source.split("<li>") if "c=" in e]

    for line in lines:
        p1 = p1search.search(line)
        p2 = p2search.search(line)
        if not (p1 and p2): continue

        catalog = p1[1].strip()
        c = p2[1].strip()
        name = p2[2].strip()

        yield (c, catalog, name)


def build(c=None):

    results = []
    
    for c1, catalog, name in findInPage(c):
        yield "%s %s" % (catalog, name)
        for subresult in build(c1):
            if not subresult.lstrip().startswith(catalog): continue
#            if subresult.startswith("\t" * 2): continue
            yield "\t%s" % subresult

    return results


count = 500
for each in build():
    count -= 1
    print(each)
    
#    if count == 0: break
