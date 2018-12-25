import board
import random

class Node:
  
  def __init__(self, qval):
    self.children = dict() 
    self.qval = qval
    

class Player:
  
  def __init__(self):
    self.root = Node(0)
    self.state = self.root

  def train(self, learnRate, discFact):
    game = board.Game()
    
    for i in range(10000000):
      currNode = self.root
      r = 0
      game.reset()
      while(r == 0):
        m = random.randint(0, 6)
        r = game.placePiece(m)
        while r == -1:
          currNode.children[m] = Node(-10000000)
          m = random.randint(0,6)
          r = game.placePiece(m)

        if m in currNode.children:
          currNode = currNode.children[m]
        else:
          currNode.children[m] = Node(0)
          currNode = currNode.children[m]

        if r != 1 and r != 2:
          m = random.randint(0, 6)
          r =  -1 * game.placePiece(m)
          while r == 1:
            m = random.randint(0,6)
            r = -1 * game.placePiece(m)

        reward = 0
        if r == 1:
          reward = 10000
        elif r == -1:
          reward = -10000 

        bestChildVal = None
        for n in currNode.children:
          node = currNode.children[n]
          if not bestChildVal or node.qval > bestChildVal:
            bestChildVal = node.qval
        if not bestChildVal or (len(currNode.children) < 7 and bestChildVal < 0):
          bestChildVal = 0

        currNode.qval = (1 - learnRate) * currNode.qval + learnRate * (reward + discFact * bestChildVal)

        if currNode.qval != 0 and currNode.qval != 3500 and currNode.qval != -3500:
          print(currNode.qval, flush=True)

        if m in currNode.children:
          currNode = currNode.children[m]
        else:
          currNode.children[m] = Node(0)
          currNode = currNode.children[m]

    print('done')

  def play(self, move):
    if move:
      if move in self.state.children:
        self.state = self.state.children[move]

    bestPlay = (0, None)

    for i in range(7):
      if i in self.state.children:
        print(i, flush=True)
        print(self.state.children[i].qval, flush=True)
        if not bestPlay[1] or self.state.children[i].qval > bestPlay[1]:
          bestPlay = (i, self.state.children[i].qval)

    return bestPlay[0]
    
  def reset(self):
    self.state = self.root

