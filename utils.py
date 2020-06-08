import math
import re
import svg.path
import ankiconnect
from kanjivg import KanjiVG
import os

pathpattern = ' d=\"(.*)\"'
pathre = re.compile(pathpattern)

def getUniPoint(ch):
    return '%05x' % ord(ch)

def splitKanji(word):
    kj = []
    for i in word:
        kvg = KanjiVG(i)
        if not kvg.svg == 0:
            kj.append(kvg)
    return kj

def parse(kvg,n=100):
    paths = [svg.path.parse_path(i) for i in pathre.findall(kvg.svg)]
    pts = [[(p.real,p.imag) for p in (path.point(i/n) for i in range(0, n+1))] for path in paths]
    return pts

def pythagDistance(a,b):
    return math.sqrt((b[0]-a[0])**2+(b[1]-a[1])**2)

def checkforkanjivg():
    if not os.path.exists("kanji"):
        print("KanjiVG data not found.")
        sys.exit()
