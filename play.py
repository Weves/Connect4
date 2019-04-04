import player
import board
import mcts

class Play:

  def __init__(self):
    self.player = player.Player()
    #self.player.qtrain(.45, .99)
    self.game = board.Game()

  def play(self):
    self.game.reset()

    while(True):

      state = board.Game(self.game.clone())
      move = mcts.search(state, 10000)

      self.game.placePiece(move)
      self.game.displayBoard()
      if self.game.victor != 0:
        break
      '''
      self.makeHumanMove()
      self.game.displayBoard()
      if self.game.victor != 0:
        break
      '''

      print('------------------------------')

      state = board.Game(self.game.clone())
      move = mcts.search(state, 20000)

      self.game.placePiece(move)
      self.game.displayBoard()
      if self.game.victor != 0:
        break

      print('------------------------------')

    print('Player ' + str(self.game.victor) + ' wins!')

  def makeHumanMove(self):
    moves = self.game.getMoves()
    while(True):
      move = input('Your turn. Please enter column # (one indexed): ')
      if int(move) < 1 or int(move) > 7:
        print('Please enter a number 1-7')
      elif (int(move) - 1) not in moves:
        print('Invalid move')
      else:
        self.game.placePiece(int(move) - 1)
        break


p = Play()

while True:
  p.play()
