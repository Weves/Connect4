import numpy as np
import math

class Game:
  def __init__(self, state = np.zeros((6, 7)), turn = 1):
    # 0 = nobody, 1 = player 1 , 2 = player 2
    self.board = state
    self.turn = turn
    self.moves = 0
    self.victor = 0
    self.heights = [5] * 7

  def reset(self):
    self.board = np.zeros((6, 7))
    self.heights = [5] * 7
    self.turn = 1
    self.moves = 0
    self.victor = 0

  def clone(self):
    return np.copy(self.board)

  def getMoves(self):
    valid = []

    if self.victor != 0:
      return valid

    for i in range(self.board.shape[1]):
      if self.board[0][i] == 0:
        valid.append(i)
    return valid

  def placePiece(self, loc):

    self.board[self.heights[loc]][loc] = self.turn
    self.moves += 1
    self.heights[loc] -= 1

    if self.checkVictory(loc, self.heights[loc] + 1, self.turn):
      self.victor = self.turn
    else:
      if self.moves >= 42:
        self.victor = 3

    self.changeTurn()

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
    tv = h - 1
    for i in range(3):
      if th < 0 or tv < 0 or self.board[tv][th] != player:
        break
      else:
        d1count += 1
        th -= 1
        tv -= 1
    th = loc + 1
    tv = h + 1
    for i in range(3):
      if th >= 7 or tv >= 6 or self.board[tv][th] != player:
        break
      else:
        d1count += 1
        th += 1
        tv += 1

    if d1count >= 4:
      return True

    th = loc - 1
    tv = h + 1
    for i in range(3):
      if th < 0 or tv >= 6 or self.board[tv][th] != player:
        break
      else:
        d2count += 1
        th -= 1
        tv += 1
    th = loc + 1
    tv = h - 1
    for i in range(3):
      if th >= 7 or tv < 0 or self.board[tv][th] != player:
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
      print(r, flush=True)

  def changeTurn(self):
    if self.turn == 1:
      self.turn = 2
    else:
      self.turn = 1

  def getResult(self, player):
    if self.victor == player:
      return 1
    elif self.victor == 3:
      return .5
    else:
      return 0
