import math
import re
import svg.path
import os
import sys
from .kanjivg import KanjiVG

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

def parse(kvg,size,n=100):
    ratio = float(size)/109
    paths = [svg.path.parse_path(i) for i in pathre.findall(kvg.svg,size)]
    pts = [[(p.real*ratio,p.imag*ratio) for p in (path.point(i/n) for i in range(0, n+1))] for path in paths]
    return pts



def pythagDistance(a,b):
    return math.sqrt((b[0]-a[0])**2+(b[1]-a[1])**2)


