
import  os
import json
import numpy as np
import tqdm

from Board import TicTacToeBoard
from MiniMax import minimaxAllContinuations
from Encode import encode


#              TableBase Concept
#########################################################
# We can pre-compute what are the best moves for every game position and store
#   ... them in a big table, a.k.a TableBase
# TableBase is a python dict with keys being the encoding of board postions
# For each position 'p', TableBase[p] is a list 'l' such that:
#       l[0] is the evalation of that position (1/0/-1 for best result being win/draw/loss)
#       l[1:] stores the best move or moves (if more than 1 move is equally best)




#       Module-Scope Variables (a.k.a globals)
#########################################################
# For any such variable:
#       Functions within this module can access it by name
#       Functions within this module can modify it by declaring this name as 'global'
#       Importing this name should be avoided; hence functions outside this module
#         ... cannot access/modify this variable.
_dataPathToDefaultTableBases = None
_AvailabeTableBases = None


def _getDataPathToDefaultTableBases():
    global _dataPathToDefaultTableBases
    
    if(_dataPathToDefaultTableBases is None):
        # Set it as a dict with paths to all the tablebases
        import Board
        rootDir = os.path.dirname(Board.__file__)  # gets the {project root 'dir'}
        _dataPathToDefaultTableBases = {
                    'minimax-1' : os.path.join(rootDir, 'data', 'TableBase_MiniMax-1.json')
                    }
    
    return _dataPathToDefaultTableBases


# A special exception used in TableBase.lookup() method
class TableBaseLookupError(LookupError):
    pass

class TableBase:
    def __init__(self):
        self.table = None
        
    def getTable(self):
        return self.table
    
    def setTable(self, newTable):
        self.table = newTable
        
    def lookup(self, idx):
        if(self.table is None):
            msg = ''
            raise RuntimeError(msg)
        try:
            return self.table[idx]
        except (KeyError,IndexError,TypeError):
            msg = ''
            raise ValueError(msg)
            
    def save(self, fpath):
        with open(fpath, "w") as jfile:
            json.dump(self.table, jfile, sort_keys=True)
    
    def load(self, fpath):
        with open(fpath, "r") as jfile:
            stringKeyTable = json.load(jfile)
            integerKeyTable = {int(i):stringKeyTable[i] for i in stringKeyTable.keys()}
            self.table = integerKeyTable


def calcTableBase_MiniMax():
    TBase = dict()
    tb = TicTacToeBoard()
    
    pbar = tqdm.tqdm(total = 294_778)
    for tb,vec in minimaxAllContinuations(tb, tb.nextTurn, tb.getOtherMark()):
        pbar.update()
        
        N = encode(tb, useSymmetry=True)[0]
        if(N == encode(tb, useSymmetry=False)):
            moves = []
            if((vec==1).any()):
                val = 1
                moves = list(np.nonzero(vec==1)[0])
            elif((vec==0).any()):
                val = 0
                moves = list(np.nonzero(vec==0)[0])
            elif((vec==-1).any()):
                val = -1
                moves = list(np.nonzero(vec==-1)[0])
            else:
                continue
            
            if(N not in TBase):
                TBase[int(N)] = [val]+[int(i) for i in moves]
    return TBase


# Out of the default table bases in _dataPthtoDefaultTableBases,
#   ... load the ones that are available on the current system.
def getAvailableTableBases():
    global _AvailabeTableBases
    if(_AvailabeTableBases is None):
        tbPaths = _getDataPathToDefaultTableBases()
        _AvailabeTableBases = {}
        for tbName in tbPaths.keys():
            try:
                tb = TableBase()
                tb.load(tbPaths[tbName])
                _AvailabeTableBases[tbName] = tb
            except FileNotFoundError:
                continue
     
    return _AvailabeTableBases
    