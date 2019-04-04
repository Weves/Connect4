import board
import random
import math

class Node:

    def __init__(self, move = None, parent = None, state = None):
        self.move = move
        self.childNodes = []
        self.wins = 0
        self.visits = 0
        self.untriedMoves = state.getMoves()
        self.playerJustMoved = 1 if state.turn == 2 else 2
        self.parentNode = parent

    def addChild(self, move, state):
        n = Node(move = move, parent = self, state = state)
        self.untriedMoves.remove(move)
        self.childNodes.append(n)
        return n

    def selectChild(self):
        s = sorted(self.childNodes, key = lambda c: c.wins/c.visits + math.sqrt(2*math.log(self.visits)/c.visits))[-1]
        return s

    def update(self, result):
        self.visits += 1
        self.wins += result


def search(rootState, iterations):

    rootNode = Node(state = rootState)

    for i in range(iterations):
        node = rootNode
        state = board.Game(rootState.clone(), rootState.turn)

        # Select
        while node.untriedMoves == [] and node.childNodes != []: # node is fully expanded and non-terminal
            node = node.selectChild()
            state.placePiece(node.move)

        # Expand
        if node.untriedMoves != []: # if we can expand (i.e. state/node is non-terminal)
            m = random.choice(node.untriedMoves)
            state.placePiece(m)
            node = node.addChild(m,state) # add child and descend tree

        # Rollout - this can often be made orders of magnitude quicker using a state.GetRandomMove() function
        while state.getMoves() != []: # while state is non-terminal
            state.placePiece(random.choice(state.getMoves()))

        # Backpropagate
        while node != None: # backpropagate from the expanded node and work back to the root node
            node.update(state.getResult(node.playerJustMoved)) # state is terminal. Update node with result from POV of node.playerJustMoved
            node = node.parentNode

    # Output some information about the tree - can be omitted

    return sorted(rootNode.childNodes, key = lambda c: c.visits)[-1].move # return the move that was most visited
