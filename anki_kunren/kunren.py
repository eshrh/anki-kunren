import argparse
import sys
import os
import svg.path
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pyg
import re
from .ankiconnect import *
from .utils import *
from .kanjivg import *




class Kunren:
    def __init__(self,char=None,field="Expression",startThreshold=10,drawThreshold=25):
        pyg.init()
        self.startThreshold = startThreshold
        self.drawThreshold = drawThreshold
        self.screen = pyg.display.set_mode((109,109))
        self.screen.fill(pyg.Color('white'))
        self.draw = False
        self.stroke = []
        self.p = (0,0) #keeps track of previous x and y of mouse to draw continuous lines.
        if char==None:
            self.exp = splitKanji(getCard(field))
        else:
            self.exp = splitKanji(char)
        print(len(self.exp))
        self.strokes = [parse(i,200) for i in self.exp]
        self.kanji = 0
        self.curstroke = 0
        self.paused = False

        while True:
            for event in pyg.event.get():
                self.inputListen(event)
            pyg.display.flip()

    def startStroke(self):
        if self.curstroke>=len(self.strokes[self.kanji]):
            self.paused = True
            return
        else:
            self.paused = False

        start = self.strokes[self.kanji][self.curstroke][0]
        if pythagDistance(start,pyg.mouse.get_pos())>self.startThreshold:
            start = [int(i) for i in self.strokes[self.kanji][self.curstroke][0]]
            pyg.draw.circle(self.screen,pyg.Color('red'),start,self.startThreshold)
        else:
            self.draw = True
            self.stroke = []
            self.p = pyg.mouse.get_pos()

    def endStroke(self):
        if self.grade(self.stroke,self.strokes[self.kanji][self.curstroke],self.drawThreshold):
            self.curstroke+=1
            self.redraw(self.kanji,self.curstroke)
        else:
            self.redraw(self.kanji,self.curstroke)
        self.draw = False

    def drawStroke(self):
        if self.draw:
            pyg.draw.aaline(self.screen,pyg.Color('red'),
                          self.p,pyg.mouse.get_pos())
            self.p = pyg.mouse.get_pos()
            self.stroke.append(pyg.mouse.get_pos())

    def correctStroke(self):
        self.redraw(self.kanji,self.curstroke)
        self.curstroke+=1

    def redraw(self,kanji,number):
        self.screen.fill(pyg.Color('white'))
        for i in range(number):
            pyg.draw.aalines(self.screen,pyg.Color('blue'),False,self.strokes[kanji][i])
    def displayNextStroke(self):
        pyg.draw.aalines(self.screen,pyg.Color('blue'),False,self.strokes[self.kanji][self.curstroke])

    def displayCurrentKanji(self,kanji):
        #broken
        pyg.draw.aalines(self.screen,pyg.Color('blue'),False,self.strokes[self.kanji])

    def hintStroke(self):
        pyg.draw.aalines(self.screen,pyg.Color('grey'),False,self.strokes[self.kanji][self.curstroke])

    def grade(self,stroke,real,thresh):
        if len(stroke)==0:
            return False
        if len(stroke)<20:
            thresh+=10
        threshold = thresh
        sumdiff = 0
        for n,i in enumerate(real):
            sumdiff += min([pythagDistance(i,j) for j in stroke])
        avg = sumdiff/len(stroke)
        return avg<=thresh

    def inputListen(self, event):
        if event.type==pyg.KEYDOWN:
            if event.key==pyg.K_n:
                if not self.kanji==len(self.exp)-1:
                    self.kanji+=1
                    self.curstroke = 0
                    self.screen.fill(pyg.Color('white'))
                    self.paused = False
            if event.key==pyg.K_h:
                self.hintStroke()
            if event.key==pyg.K_ESCAPE:
                sys.exit()
        if not self.paused:
            if event.type == pyg.MOUSEBUTTONDOWN:
                self.startStroke()
            if event.type == pyg.MOUSEBUTTONUP:
                self.endStroke()
            if event.type == pyg.MOUSEMOTION:
                self.drawStroke()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s',default=5,type=int,help="Start point size in px. default 5px")
    parser.add_argument('-d',default=25,type=int,help="Stroke forgiveness in average px from actual. default 25px")
    parser.add_argument('--field',default="Expression",type=str,help="name of anki card field containing kanji")
    args = vars(parser.parse_args())
    kunren = Kunren(startThreshold=args['s'],drawThreshold=args['d'],field=args['field'])


main()
