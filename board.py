import numpy as np
import math

class Game:
  def __init__(self):
    # 0 = nobody, 1 = player 1 , 2 = player 2
    self.board = np.zeros((6, 7))
    self.turn = 1
    self.moves = 0

  def reset(self):
    self.board = np.zeros((6, 7))
    self.turn = 1
    self.moves = 0
  
  def placePiece(self, loc):
    h = 5

    while self.board[h][loc]:
      h -= 1
      if h < 0:
        break
    if h >= 0:
      self.moves += 1
      self.board[h][loc] = self.turn
      if self.checkVictory(loc, h, self.turn):
        return 1
      else:
        self.changeTurn()
        if self.moves >= 42:
          return 2
        else:
          return 0
    else:
      return -1

  def checkVictory(self, loc, h, player):

    vcount = 1
    hcount = 1
    d1count = 1
    d2count = 1

    t = h - 1
    for i in range(3):
      if t < 0 or self.board[t][loc] != player:
        break
      else:
        vcount += 1
        t -= 1
    t = h + 1
    for i in range(3):
      if t >= 6 or self.board[t][loc] != player:
        break
      else:
        vcount += 1
        t += 1
    
    if vcount >= 4:
      return True

    t = loc - 1
    for i in range(3):
      if t < 0 or self.board[h][t] != player:
        break
      else:
        hcount += 1
        t -= 1
    t = loc + 1
    for i in range(3):
      if t >= 7 or self.board[h][t] != player:
        break
      else:
        hcount += 1
        t += 1
    
    if hcount >= 4:
      return True

    th = loc - 1
    tv = t - 1
    for i in range(3):
      if th < 0 or tv < 0 or self.board[th][tv] != player:
        break
      else:
        d1count += 1
        th -= 1
        tv -= 1
    th = loc + 1
    tv = t + 1
    for i in range(3):
      if th >= 7 or tv >= 6 or self.board[th][tv] != player:
        break
      else:
        d1count += 1
        th += 1
        tv += 1
    
    if d1count >= 4:
      return True

    th = loc - 1
    tv = t + 1
    for i in range(3):
      if th < 0 or tv >= 6 or self.board[th][tv] != player:
        break
      else:
        d2count += 1
        th -= 1
        tv += 1
    th = loc + 1
    tv = t - 1
    for i in range(3):
      if th <= 7 or tv < 0 or self.board[th][tv] != player:
        break
      else:
        d2count += 1
        th += 1
        tv -= 1
    
    if d2count >= 4:
      return True


    return False

  def displayBoard(self):
    for r in self.board:
      print(r)

  def changeTurn(self):
    if self.turn == 1:
      self.turn = 2
    else:
      self.turn = 1



      

