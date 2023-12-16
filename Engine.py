
import numpy as np

from Board import TicTacToeBoard
from MiniMax import minimaxEvalsForNextMoves
from Encode import encode
from Symmetry import newIndex
from TableBase import TableBaseLookupError


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
             
    
    # Generate a random next move
    def randomMove(self, tb : TicTacToeBoard):
        candidateMoves = tb.possibleNextMoves()
        if(len(candidateMoves)==0):
            msg = "The given board is already filled in call to randomMove()"
            raise ValueError(msg)
        else:
            return self.chooseAmongCandidates(candidateMoves, 'random')
        
    # A helper function 
    def chooseAmongCandidates(self, candidateMoves, separateEqualsBy='random'):
        if(separateEqualsBy not in ['random', 'leftmost', 'rightmost']):
            msg = "Argument 'separateEqualsBy' in call to Engine.method() must " + \
                    "either be left out or be one of " + \
                    "['random', 'leftmost', 'rightmost']. " + \
                    "Received '{}'".format(separateEqualsBy)
            raise ValueError(msg)
            
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
            
            
    # Pick the best move in the current position
    # Resolve ties as either first, last or random choice.
    def bestMove(self, tb:TicTacToeBoard, separateEqualsBy='random'):            
        candidateMoves = self.listBestMoves(tb)
        return self.chooseAmongCandidates(candidateMoves, separateEqualsBy)            
###############################################################################
          



#        Engine that uses the Mini-Max algorithm    
###############################################################################
class MiniMaxEngine(TicTacToeEngine):
    
    def __init__(self, pruning=True, randomSeed=None, rng=None):
        super().__init__(randomSeed, rng)        
        self.pruning = pruning
      
        
    # Use the minimax algorithm (w/ or w/o pruning) to find all the moves
    #   ... that lead to the best possible result for the next player
    def listBestMoves(self, tb):
        
        orig = tb
        tb = TicTacToeBoard(copyFrom=orig)
        
        scores = minimaxEvalsForNextMoves(tb, pruning=self.pruning)
        
        winningScore = (1 if(tb.nextTurn==tb.Xmark) else -1)
        losingScore = (-1 if(tb.nextTurn==tb.Xmark) else 1)
        # drawingScore is always 0
        
        if(np.any(scores==winningScore)):
            bestCandidates = np.nonzero(scores==winningScore)[0]
        elif(np.any(scores==0)):
            bestCandidates = np.nonzero(scores==0)[0]
        elif(np.any(scores==losingScore)):
            bestCandidates = np.nonzero(scores==losingScore)[0]
        else:
            msg = ("The engine found no valid moves. Board: {}, " + \
                    "Minimax scores: {}").format(tb.board, scores)
            raise RuntimeError(msg)
        
        return bestCandidates
###############################################################################




#        Engine that uses the Saved TableBase
###############################################################################
class TableBaseEngine(TicTacToeEngine):
    
    def __init__(self, tableBase, randomSeed=None, rng=None):
        super().__init__(randomSeed, rng)
        self.tbase = tableBase
        
    # Use the tablebase and the appropriate transformation fn. to lookup 
    #   ... all the moves for the next player that lead to the best result
    def listBestMoves(self, tb:TicTacToeBoard):
        
        N,op = encode(tb, useSymmetry=True)
        try:
            ls = self.tbase.lookup(N)
        except TableBaseLookupError:
            msg = "In call to TableBaseEngine.bestMove(), the position " +\
                    "{}, encoded as {}, was not found in the tablebase."
            msg = msg.format(tb.board, N)
            raise TableBaseLookupError(msg)
        
        candidateMoves = [newIndex(i, op) for i in ls[1:]]
        
        candidateMoves = np.array(candidateMoves, dtype=np.uint8)
        return candidateMoves
###############################################################################                         
