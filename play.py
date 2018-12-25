import player
import board

class Play:
  
  def __init__(self):
    self.player = player.Player()
    self.player.train(.35, 1)
    self.game = board.Game()
    self.playerMove = None
  
  def play(self):
    self.game.reset()
    board = player.Node('11111111111111', 0)
    while(True):
      play = self.player.play(board.boardState)
      board = player.Node(board.findNext(play, 1), 0)
      r = self.game.placePiece(play)
      if r == 1:
        break
      r = self.getMove()
      board = player.Node(board.findNext(self.playerMove, 2), 0)
      if r:
        break
    print(r)

  def getMove(self):
    self.game.displayBoard()
    while(True):
      move = input('Your turn. Please enter column # (one indexed): ')
      if int(move) < 1 or int(move) > 7:
        print('Please enter a number 1-7')
      else:
        self.playerMove = int(move) - 1
        res = self.game.placePiece(int(move) - 1)
        if res != -1:
          return res

p = Play()

while True:
  p.play()
