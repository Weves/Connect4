import math
import copy
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
    self.nn = MLPClassifier(hidden_layer_sizes=(14, 5))
    self.MAX_DEPTH = 10
    self.root = Node('11111111111111', 0)
    self.state = self.root
    self.nodeList = {'11111111111111' : self.root}

  def train(self, learnRate, discFact):

    # train basic qlearning model to get nn started
 
    self.qtrain(learnRate, discFact)

    game = board.Game()

    for i in range(10000):
      currNode = self.root
      currState = '11111111111111'
      r = 0
      game.reset()
      depth = 0
      while(r == 0):
        
        r = -1
        while r == -1:
          if depth < self.MAX_DEPTH:
            m = self.qplay(currNode.boardState)
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

        if i % 10000 == 0:
          dinc += 1
          print(i, flush=True)

 
    for i in range(10000):
      currNode = self.root
      seenStates = []
      r = 0
      game.reset()
      while(r == 0):

        r = -1
        rando = False
        while r == -1:
          if not rando and i > 5000:
            m = self.play(game.board)
            rando = True
          else:
            m = random.randint(0,6)
          r = game.placePiece(m)

        seenStates.append(game.board.ravel())

        if r != 1 and r != 2:
          r = 1
          rando = False
          while r == 1:
            if not rando and i > 5000:
              m = self.play(game.board, player=2)
              rando = True
            else:
              m = random.randint(0,6)
            r = -1 * game.placePiece(m)

        if r == -2:
          r = 2

        seenStates.append(game.board.ravel())

      self.nn.partial_fit(seenStates, [r] * len(seenStates), [-1, 1, 2])
    
  def play(self, state, debug=False, player=1):

    ind = 1 if player == 1 else 0

    t_game = board.Game()
    p_states = []
    for i in range(7):
      t_game.board = copy.deepcopy(state)
      t_game.turn = 1
      t_game.placePiece(i)
      p_states.append(copy.deepcopy(t_game.board.ravel()))
    
    p = self.nn.predict_proba(p_states)
    if debug:
      print(p_states, flush=True)
      print(p, flush=True)

    bestPlay = (0, p[0][ind])
    for i in range(1, 7):
      if p[i][ind] > bestPlay[1]:
        bestPlay = (i, p[i][1])

    return bestPlay[0]

  
  
  
  def bestChild(self, node, player):
    bestChildVal = None
    seen = 0
    for n in range(7):
      nState = node.findNext(n, player)
      if nState in self.nodeList:
        if not bestChildVal or self.nodeList[nState].qval > bestChildVal:
          bestChildVal = self.nodeList[nState].qval
      else:
        if not bestChildVal or 0 > bestChildVal:
          bestChildVal = 0
    return bestChildVal

  def qtrain(self, learnRate, discFact):
    
    game = board.Game()
    
    for i in range(500000):
      currNode = self.root
      r = 0
      game.reset()
      while(r == 0):

        pNode = currNode

        r = -1
        while r == -1:
          m = random.randint(0,6)
          r = game.placePiece(m)
          newKey = currNode.findNext(m, 1)
          if r == -1:
            self.nodeList[newKey] = Node(newKey, -10000000)  

        if newKey not in self.nodeList:
          self.nodeList[newKey] = Node(newKey, 0)
    
        tNode = self.nodeList[newKey]

        if r != 1 and r != 2:
          r = 1
          while r == 1:
            m = random.randint(0,6)
            r = -1 * game.placePiece(m)
            newKey = tNode.findNext(m, 2)
            if r == 1:
              self.nodeList[newKey] = Node(newKey, -1000000)

        if newKey not in self.nodeList:
          self.nodeList[newKey] = Node(newKey, 0)

        currNode = self.nodeList[newKey]
    
        reward = 0
        if r == 1:
          reward = 100
        elif r == -1:
          reward = -100 
      
        bestChildVal = self.bestChild(tNode, 2)
      
        #average reward from this position for player 2
        pNode.seen += 1
        pNode.qval = (pNode.seen - 1) / pNode.seen * pNode.qval + (-1 * reward + discFact * bestChildVal) / pNode.seen

        bestChildVal = self.bestChild(currNode, 1)

        #average reward from this position for player 1
        tNode.seen += 1
        tNode.qval = (tNode.seen - 1) / tNode.seen * tNode.qval + (reward + discFact * bestChildVal) / tNode.seen
        
        #if pNode.qval != 0:
        #  print(pNode.qval)
        #if tNode.qval != 0:
        #  print(tNode.qval)

    print('Done with random training', flush=True)
    
    dinc = 0
    for i in range(100000):
      currNode = self.root
      currState = '11111111111111'
      r = 0
      game.reset()
      depth = 0
      while(r == 0):

        pNode = currNode
        
        depth += 1

        r = -1
        while r == -1:
          if depth < 5 + dinc:
            m = self.qplay(currNode.boardState)
          else:
            m = random.randint(0, 6)
          r = game.placePiece(m)
          newKey = currNode.findNext(m, 1)
          if r == -1:
            self.nodeList[newKey] = Node(newKey, -10000000)  

        if newKey not in self.nodeList:
          self.nodeList[newKey] = Node(newKey, 0)
    
        tNode = self.nodeList[newKey]

        if r != 1 and r != 2:
          r = 1
          while r == 1:
            if depth < 5 + dinc:
              m = self.qplay(tNode.boardState)
            else:
              m = random.randint(0,6)
            r = -1 * game.placePiece(m)
            newKey = tNode.findNext(m, 2)
            if r == 1:
              self.nodeList[newKey] = Node(newKey, -10000000)  

        if newKey not in self.nodeList:
          self.nodeList[newKey] = Node(newKey, 0)

        currNode = self.nodeList[newKey]

        reward = 0
        if r == 1:
          reward = 100
        elif r == -1:
          reward = -100 

        bestChildVal = self.bestChild(tNode, 2)

        # updating qlearning val for player 2
        pNode.qval = (1 - learnRate) * pNode.qval + learnRate * (reward + discFact * bestChildVal)

        bestChildVal = self.bestChild(currNode, 1)

        # updating qlearning val for player 1
        tNode.qval = (1 - learnRate) * tNode.qval + learnRate * (reward + discFact * bestChildVal)

      if i % 10000 == 0:
        dinc += 1
        print(i, flush=True)

    print('done', flush=True)

  def qplay_r(self, state):

    plays = []

    for i in range(7):
      nState = tNode.findNext(i, 1)
      if nState in self.nodeList:
        plays.append((i, self.nodeList[nState.qval]))
      else:
        plays.append((i, 0))

    plays.sort(key = lambda x : x[1], reverse = True)
    num = random.randint(0, 25)
    if num < 7:
      return plays[0][0]
    elif num < 13:
      return plays[1][0]
    elif num < 18:
      return plays[2][0]
    elif num < 22:
      return plays[3][0]
    else:
      return plays[4][0]

  def qplay(self, state, debug=False):

    bestPlay = (random.randint(0, 6), None)
    tNode = Node(state, 0)

    for i in range(7):
      nState = tNode.findNext(i, 1)
      if debug:
        print(nState, flush=True)
      if nState in self.nodeList:
        if debug:
          print(self.nodeList[nState].qval)
          print(self.nodeList[nState].seen)
        if not bestPlay[1] or self.nodeList[nState].qval > bestPlay[1]:
          bestPlay = (i, self.nodeList[nState].qval)
      else:
        if bestPlay[1] and 0 > bestPlay[1]:
          bestPlay = (i, 0)

    return bestPlay[0]

  def reset(self):
    self.state = self.root


