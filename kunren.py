import time
import sys
import numpy
from ankiconnect import *
from utils import *
from kanjivg import *
import os
import svg.path

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pyg
import re



class Kunren:
    def __init__(self,char=0):
        checkforkanjivg()
        pyg.init()
        self.startThreshold = 10
        self.drawThreshold = 25
        self.screen = pyg.display.set_mode((109,109))
        self.screen.fill(pyg.Color('white'))
        self.draw = False
        self.stroke = []
        self.p = (0,0) #keeps track of previous x and y of mouse to draw continuous lines.
        if char==0:
            self.exp = splitKanji(getCard())
        else:
            self.exp = splitKanji(char)
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
            self.screen.fill(pyg.Color('white'))
            self.curstroke+=1
            self.displayAllStrokesUntil(self.kanji,self.curstroke)
        else:
            self.screen.fill(pyg.Color('white'))
            self.displayAllStrokesUntil(self.kanji,self.curstroke)
        self.draw = False

    def drawStroke(self):
        if self.draw:
            pyg.draw.aaline(self.screen,pyg.Color('red'),
                          self.p,pyg.mouse.get_pos())
            self.p = pyg.mouse.get_pos()
            self.stroke.append(pyg.mouse.get_pos())

    def correctStroke(self):
        self.screen.fill(pyg.Color('white'))
        self.displayNextStroke()
        self.curstroke+=1

    def displayAllStrokesUntil(self,kanji,number):
        for i in range(number):
            pyg.draw.aalines(self.screen,pyg.Color('blue'),False,self.strokes[kanji][i])
    def displayNextStroke(self):
        pyg.draw.aalines(self.screen,pyg.Color('blue'),False,self.strokes[self.kanji][self.curstroke])
    def displayCurrentKanji(self,kanji):
        pyg.draw.aalines(self.screen,pyg.Color('blue'),self.strokes[self.kanji])

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
            if event.key==pyg.K_c:
                self.screen.fill(pyg.Color('white'))
                self.displayAllStrokesUntil(self,self.kanji,self.curstroke)
            if event.key==pyg.K_n:
                if not self.kanji==len(self.exp)-1:
                    self.kanji+=1
                    self.curstroke = 0
                    self.screen.fill(pyg.Color('white'))
                    self.paused = False
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
    #kunren = Kunren("今日")
    kunren = Kunren()

main()
