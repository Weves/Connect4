import math
from sklearn.neural_network import MLPClassifier

import board
import random


class Node:
  
  def __init__(self, state, qval):
    self.boardState = state
    self.children = dict() 
    self.qval = qval
    self.seen = 0

  def findNext(self, m, player):
    one_val = ord(self.boardState[m * 2]) - 48
    one_height = int((one_val + 1) / 2)
    two_val = ord(self.boardState[m * 2 + 1]) - 48
    two_height = int((two_val + 1) / 2)
    tot_height = one_height + two_height
    if player == 1:
      return self.boardState[:m * 2] + chr(one_val * 2 + 48) + self.boardState[m * 2 + 1:]
    else:
      return self.boardState[:m * 2 + 1] + chr(two_val * 2 + 48) + self.boardState[m * 2 + 2:]

class Player:
  
  def __init__(self):
    self.nn = MLPClassifier(hidden_layer_sizes=(14, 4))
    self.MAX_DEPTH = 10
    self.root = Node('11111111111111', 0)
    self.state = self.root
    self.nodeList = {'11111111111111' : self.root}

  def train(self, learnRate, discFact):
    game = board.Game()
    
    for i in range(1000000):
      currNode = self.root
      currState = '11111111111111'
      seenStates = []
      r = 0
      game.reset()
      while(r == 0):

        r = -1
        while r == -1:
          m = random.randint(0,6)
          r = game.placePiece(m)
          newKey = currNode.findNext(m, 1)
          if r == -1:
            self.nodeList[newKey] = Node(newKey, -10000000)  

        if newKey not in self.nodeList:
          self.nodeList[newKey] = Node(newKey, 0)
    
        currNode = self.nodeList[newKey]

        if r != 1 and r != 2:
          r = 1
          while r == 1:
            m = random.randint(0,6)
            r = -1 * game.placePiece(m)

        currState = currNode.findNext(m, 2)
        tNode = Node(currState, 0)

        reward = 0
        if r == 1:
          reward = 100
        elif r == -1:
          reward = -100 

        bestChildVal = None
        seen = 0
        for n in range(7):
          nState = tNode.findNext(n, 1)
          if nState in self.nodeList:
            if not bestChildVal or self.nodeList[nState].qval > bestChildVal:
              bestChildVal = self.nodeList[nState].qval
          else:
            if not bestChildVal or 0 > bestChildVal:
              bestChildVal = 0

#        currNode.qval = (1 - learnRate) * currNode.qval + learnRate * (reward + discFact * bestChildVal)
        currNode.seen += 1
        currNode.qval = (currNode.seen - 1) / currNode.seen * currNode.qval + (reward + discFact * bestChildVal) / currNode.seen

        currNode = tNode

    dinc = 0
    for i in range(100000):
      currNode = self.root
      currState = '11111111111111'
      r = 0
      game.reset()
      depth = 0
      while(r == 0):
        
        depth += 1

        r = -1
        while r == -1:
          if depth < 5:
            m = self.play(currNode.boardState)
          else:
            m = random.randint(0, 6)
          r = game.placePiece(m)
          newKey = currNode.findNext(m, 1)
          if r == -1:
            self.nodeList[newKey] = Node(newKey, -10000000)  

        if newKey not in self.nodeList:
          self.nodeList[newKey] = Node(newKey, 0)
    
        currNode = self.nodeList[newKey]

        if r != 1 and r != 2:
          r = 1
          while r == 1:
            m = random.randint(0,6)
            r = -1 * game.placePiece(m)

        currState = currNode.findNext(m, 2)
        tNode = Node(currState, 0)

        reward = 0
        if r == 1:
          reward = 100
        elif r == -1:
          reward = -100 

        bestChildVal = None
        seen = 0
        for n in range(7):
          nState = tNode.findNext(n, 1)
          if nState in self.nodeList:
            if not bestChildVal or self.nodeList[nState].qval > bestChildVal:
              bestChildVal = self.nodeList[nState].qval
          else:
            if not bestChildVal or 0 > bestChildVal:
              bestChildVal = 0

        currNode.qval = (1 - learnRate) * currNode.qval + learnRate * (reward + discFact * bestChildVal)
        currNode.seen += 1
        #currNode.qval = (currNode.seen - 1) / currNode.seen * currNode.qval + (reward + discFact * bestChildVal) / currNode.seen

        currNode = tNode

        if i % 10000 == 0:
          dinc += 1
          print(i, flush=True)

  def play(self, state, debug=False):

    bestPlay = (random.randint(0, 6), None)
    tNode = Node(state, 0)

    for i in range(7):
      nState = tNode.findNext(i, 1)
      if debug:
        print(nState, flush=True)
      if nState in self.nodeList:
        if debug:
          print(self.nodeList[nState].qval)
        if not bestPlay[1] or self.nodeList[nState].qval > bestPlay[1]:
          bestPlay = (i, self.nodeList[nState].qval)
      else:
        if bestPlay[1] and 0 > bestPlay[1]:
          bestPlay = (i, 0)

    return bestPlay[0]
    
  def reset(self):
    self.state = self.root


