import math

import board
import random


class Node:
  
  def __init__(self, state, qval):
    self.boardState = state
    self.children = dict() 
    self.qval = qval

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
    self.MAX_DEPTH = 10
    self.root = Node('11111111111111', 0)
    self.state = self.root
    self.nodeList = {'11111111111111' : self.root}
    self.nodeLayers = [{'11111111111111': self.root}]
    for i in range(self.MAX_DEPTH):
      self.nodeLayers.append({})

  def train(self, learnRate, discFact):
    game = board.Game()
    
    for i in range(500000):
      currNode = self.root
      currState = '11111111111111'
      r = 0
      game.reset()
      depth = 0
      while(r == 0):

        m = random.randint(0, 6)
        r = game.placePiece(m)
        newKey = currNode.findNext(m, 1)
        while r == -1:
          if newKey not in self.nodeList:
            self.nodeList[newKey] = Node(newKey, -10000000)
          
          m = random.randint(0,6)
          r = game.placePiece(m)
          newKey = currNode.findNext(m, 1)

        if newKey not in self.nodeList:
          self.nodeList[newKey] = Node(newKey, 0)
    
        currNode = self.nodeList[newKey]

        if r != 1 and r != 2:
          m = random.randint(0, 6)
          r =  -1 * game.placePiece(m)
          while r == 1:
            m = random.randint(0,6)
            r = -1 * game.placePiece(m)

        currState = currNode.findNext(m, 2)
        tNode = Node(currState, 0)

        reward = 0
        if r == 1:
          reward = 10000
        elif r == -1:
          reward = -10000 

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
      
        currNode = tNode
        #if currNode.qval != 0 and currNode.qval != 3500 and currNode.qval != -3500:
        #  print(currNode.qval, flush=True)

    print('done')

  def play(self, state):

    bestPlay = (0, None)
    tNode = Node(state, 0)

    for i in range(7):
      nState = tNode.findNext(i, 1)
      print(nState, flush=True)
      if nState in self.nodeList:
        print(self.nodeList[nState].qval)
        if not bestPlay[1] or self.nodeList[nState].qval > bestPlay[1]:
          bestPlay = (i, self.nodeList[nState].qval)
      else:
        if not bestPlay[1] or 0 > bestPlay[1]:
          bestPlay = (i, 0)

    return bestPlay[0]
    
  def reset(self):
    self.state = self.root


