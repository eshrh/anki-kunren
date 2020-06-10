import time
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
    def __init__(self,char=None,field="Expression",startThreshold=None,drawThreshold=None,size=109):
        pyg.init()
        self.size = size
        self.startThreshold = int(startThreshold*(size/109))
        self.drawThreshold = int(drawThreshold*(size/109))
        self.nstrokes = int(200*(size/109))
        self.field = field
        self.screen = pyg.display.set_mode((size,size))
        self.screen.fill(pyg.Color('white'))
        self.draw = False
        self.stroke = []
        self.p = (0,0) #keeps track of previous x and y of mouse to draw continuous lines.
        if char==None:
            self.card = getCard(field)
            self.exp = splitKanji(self.card)
        else:
            self.exp = splitKanji(char)

        self.strokes = self.getStrokes()
        self.kanji = 0
        self.curstroke = 0
        self.error = [0,0] #misstarts,total pixel error
        self.paused = False
        self.segment = 0

        while True:
            if self.paused:
                if self.kanji<len(self.exp)-1:
                    self.nextKanji()
                else:
                    newcard = getCard(self.field)
                    if newcard != self.card:
                        self.newCard(newcard)

            for event in pyg.event.get():
                self.inputListen(event)
            pyg.display.flip()

    def getStrokes(self):
        return [parse(i,self.size,self.nstrokes) for i in self.exp]

    def newCard(self,card):
        self.card = card
        self.exp = splitKanji(self.card)
        self.strokes = self.getStrokes()
        self.paused = False
        self.kanji,self.curstroke = 0,0
        self.redraw(self.kanji,self.curstroke)

    def nextKanji(self):
        time.sleep(0.1)
        self.printSummary()
        self.curstroke=0
        self.kanji+=1
        self.error = [0,0]

        if self.kanji>len(self.exp)-1:
            self.paused=True
            return
        else:
            self.paused=False

        self.redraw(self.kanji,self.curstroke)

    def printSummary(self):
        print("kanji:",self.exp[self.kanji].character,
              "finished | misstarts:",self.error[0],
              "avg px error:",self.error[1]/len(self.strokes[self.kanji]))

    def startStroke(self):
        if self.paused:
            return
        start = self.strokes[self.kanji][self.curstroke][0]
        if pythagDistance(start,pyg.mouse.get_pos())>self.startThreshold:
            start = [int(i) for i in self.strokes[self.kanji][self.curstroke][0]]
            pyg.draw.circle(self.screen,pyg.Color('red'),start,self.startThreshold)
            self.error[0]+=1
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
        self.checkPause()

    def checkPause(self):
        if self.curstroke==len(self.strokes[self.kanji]):
            self.paused = True

    def drawStroke(self):
        if self.draw:
            pyg.draw.aaline(self.screen,pyg.Color('red'),
                          self.p,pyg.mouse.get_pos())
            self.p = pyg.mouse.get_pos()
            self.stroke.append(pyg.mouse.get_pos())

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
        if self.curstroke<len(self.strokes[self.kanji]):
            pyg.draw.aalines(self.screen,pyg.Color('grey'),False,self.strokes[self.kanji][self.curstroke])
        #TODO slow draw hints

    def animateStroke(self,kj,stroke):
        if self.segment>=len(self.strokes[kj][stroke])-2:
            self.segment=0
            self.curstroke+=1
            pyg.time.set_timer(pyg.USEREVENT,0)
            self.checkPause()
            return

        pyg.draw.aaline(self.screen,pyg.Color('blue'),
                        self.strokes[kj][stroke][self.segment],self.strokes[kj][stroke][self.segment+1])
            #time.sleep(10)

        self.segment+=1
        pyg.time.set_timer(pyg.USEREVENT,10)




    def grade(self,stroke,real,thresh):
        if len(stroke)==0:
            return False
        threshold = thresh
        sumdiff = 0
        for n,i in enumerate(real):
            sumdiff += min([pythagDistance(i,j) for j in stroke])
        avg = sumdiff/len(stroke)
        if avg<=thresh:
            self.error[1]+=avg
        return avg<=thresh

    def inputListen(self, event):
        if event.type==pyg.USEREVENT:
            self.animateStroke(self.kanji,self.curstroke)

        if event.type==pyg.KEYDOWN:
            if event.key==pyg.K_n:
                if not self.kanji==len(self.exp)-1:
                    self.nextKanji()
            if event.key==pyg.K_c:
                self.newCard(getCard(self.field))
            if event.key==pyg.K_h:
                self.hintStroke()
            if event.key==pyg.K_a:
                self.animateStroke(self.kanji,self.curstroke)
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
    parser.add_argument('--size',default=300,type=int,help="Length of the side of square canvas. Default 300px")
    args = vars(parser.parse_args())
    kunren = Kunren(startThreshold=args['s'],drawThreshold=args['d'],field=args['field'],size=args['size'])


main()
