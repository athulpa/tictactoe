
import numpy as np

from Board import TicTacToeBoard
from MiniMax import minimax


#        Base Class for all TicTacToe engines
###############################################################################
class TicTacToeEngine:
    # Constuctor accepts either an RNG or a seed value
    def __init__(self, randomSeed=None, rng=None):
        if(rng is not None):
            self.rng = rng
        else:
            if(randomSeed is not None):
                self.rng = np.random.default_rng(seed=randomSeed)
            else:
                self.rng = np.random.default_rng()
             
    def bestMove(self, tb:TicTacToeBoard, separateEqualsBy='random'):
        msg = "bestMove() is an abstract method for this class. " + \
                "Must call this method on one of the child classes."
        raise NotImplementedError(msg)
        
        
    # Generate a random next move
    def randomMove(self, tb:TicTacToeBoard):
        candidateMoves = tb.possibleNextMoves()
        if(len(candidateMoves)==0):
            msg = "The given board is already filled in call to randomMove()"
            raise ValueError(msg)
        else:
            rndIdx = self.rng.integers(len(candidateMoves))
            return candidateMoves[rndIdx]
###############################################################################
          



#        Engine that uses the Mini-Max algorithm      
###############################################################################
class MiniMaxEngine(TicTacToeEngine):
    
    def __init__(self, randomSeed=None, rng=None):
        super(randomSeed, rng)        
        
        
    # After running minimax(), pick the best move
    # Resolve ties as either first, last or random choice.
    def bestMove(self, tb:TicTacToeBoard, separateEqualsBy='random'):
        if(separateEqualsBy not in ['random', 'leftmost', 'rightmost']):
            msg = "Argument 'separateEqualsBy' in call to bestMove() must " + \
                    "either be left out or be one of " + \
                    "['random', 'leftmost', 'rightmost']. " + \
                    "Received '{}'".format(separateEqualsBy)
            raise ValueError(msg)
            
        orig = tb
        tb = TicTacToeBoard(copyFrom=orig)
        
        scores = minimax(tb, myMark=tb.nextTurn, otherMark=tb.getOtherMark())
        if(np.any(scores==1)):
            candidateMoves = np.nonzero(scores==1)[0]
        elif(np.any(scores==0)):
            candidateMoves = np.nonzero(scores==0)[0]
        elif(np.any(scores==-1)):
            candidateMoves = np.nonzero(scores==-1)[0]
        else:
            msg = ("The engine found no valid moves. Board: {}, " + \
                    "Minimax scores: {}").format(tb.board, scores)
            raise RuntimeError(msg)
            
        if(len(candidateMoves)==1):
            return candidateMoves[0]
        else:
            if(separateEqualsBy=='leftmost'):
                return candidateMoves[0]
            elif(separateEqualsBy=='rightmost'):
                return candidateMoves[-1]
            elif(separateEqualsBy=='random'):
                rndIdx = self.rng.integers(len(candidateMoves))
                return candidateMoves[rndIdx]
###############################################################################                   