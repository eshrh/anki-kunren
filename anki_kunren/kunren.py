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
        self.startThreshold = int(startThreshold*(size/109)) #scale up thresholds
        self.drawThreshold = int(drawThreshold*(size/109))
        self.nstrokes = int(200*(size/109))
        self.field = field
        self.screen = pyg.display.set_mode((size,size))
        self.screen.fill(pyg.Color('white'))
        self.draw = False
        self.stroke = []
        self.p = (0,0) #keeps track of previous x and y of mouse to draw continuous lines.
        # actually get the card from anki connect here
        if char==None:
            self.card = getCard(field)
            self.exp = splitKanji(self.card)
        else:
            self.exp = splitKanji(char)

        self.strokes = self.getStrokes()
        self.kanji = 0 #index of current kanji
        self.curstroke = 0 #index of current stroke
        self.error = [0,0] #misstarts,total pixel error
        self.paused = False #we check for new cards and finished kanji when paused, and disable all user drawing.
        self.segment = 0 # used in animating strokes
        self.currentlyAnimating = False # used in animating all strokes to detect when finished
        self.curAnimateStroke = -1 #index of currently animating stroke. -1 because it will start by incrementing.

        while True:
            #check for new cards and finished kanji while paused
            if self.paused:
                if self.kanji<len(self.exp)-1:
                    self.nextKanji()
                else:
                    newcard = getCard(self.field)
                    if newcard != self.card:
                        self.newCard(newcard)

            # get and process all user input, then update the screen.
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
        #prints summary of kanji drawing.
        print("kanji:",self.exp[self.kanji].character,
              "finished | misstarts:",self.error[0],
              "avg px error:",self.error[1]/len(self.strokes[self.kanji]))

    def startStroke(self):
        #starts a stroke, which must be within the start circle.
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
        #finish the stroke
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

    def hintStroke(self):
        if self.curstroke<len(self.strokes[self.kanji]):
            pyg.draw.aalines(self.screen,pyg.Color('grey'),False,self.strokes[self.kanji][self.curstroke])

    def animateStroke(self,kj,stroke):
        #basically a stacked queue of events that sequentially draws segments of a line
        #while not blocking user input.
        if self.segment>=len(self.strokes[kj][stroke])-2:
            self.segment=0
            self.curstroke+=1
            pyg.time.set_timer(pyg.USEREVENT,0)
            self.checkPause()
            self.currentlyAnimating = False
            return

        self.currentlyAnimating=True
        pyg.draw.aaline(self.screen,pyg.Color('blue'),
                        self.strokes[kj][stroke][self.segment],self.strokes[kj][stroke][self.segment+1])
        self.segment+=1
        pyg.time.set_timer(pyg.USEREVENT,10)

    def animateAll(self,kanji):
        #another event stack that manages animateStroke()
        if self.curAnimateStroke>=len(self.strokes[kanji])-1:
            self.curAnimateStroke = -1
            pyg.time.set_timer(pyg.USEREVENT+1,0)
            return
        if self.currentlyAnimating==False:
            self.curAnimateStroke+=1
            self.animateStroke(kanji,self.curAnimateStroke)
        pyg.time.set_timer(pyg.USEREVENT+1,200)

    def grade(self,stroke,real,thresh):
        #check if average minimum errors is lesser than the forgiveness.
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
        if event.type==pyg.USEREVENT+1:
            self.animateAll(self.kanji)
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
            if event.key==pyg.K_d:
                self.animateAll(self.kanji)
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
    parser.add_argument('--field',default="Vocabulary-Kanji",type=str,help="name of anki card field containing kanji. Defaults to \"Vocabulary-Kanji\"")
    parser.add_argument('--size',default=300,type=int,help="Length of the side of square canvas. Default 300px")
    args = vars(parser.parse_args())
    kunren = Kunren(startThreshold=args['s'],drawThreshold=args['d'],field=args['field'],size=args['size'])

main()
