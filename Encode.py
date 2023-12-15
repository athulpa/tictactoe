
import os
import numpy as np

from Board import TicTacToeBoard
from Symmetry import transformVec, allVectorVariants
from Helper import makeBoardFromIllegalPosition, moduleDir


#       Simple Encoding/Decoding functions
######################################################
def _encodeBoardAsInteger(tb : TicTacToeBoard) -> int:
    return np.sum(tb.board*(3**np.arange(9)))

def _decodeBoardFromInteger(N : int) -> TicTacToeBoard:
    return makeBoardFromIllegalPosition((N//3**(np.arange(9)))%3)

def _encodeVectorAsInteger(vec):
    return np.sum(vec*(3**np.arange(9)))

def _decodeVectorFromInteger(N):
    return (N//3**(np.arange(9)))%3
######################################################



#       Module-Scope Variables (a.k.a globals)
#########################################################
# For any such variable:
#       Functions within this module can access it by name
#       Functions within this module can modify it by declaring this name as 'global'
#       Importing this name should be avoided; hence functions outside this module
#         ... cannot access/modify this variable.
_SymTable = None
_dataPathToSymTable = None




#        SYMMETRY TABLE CONCEPT
######################################

# For any board position, flipping and/or rotating it again and again can
#   ... create upto 8 unique board positions (including the original)
# Since these symmetric boards have a lot in common with each other, we can
#   ... take advantage of that while encoding.
# 
# To capture which boards are symmetric to which others, we create a Symmetry Table.
# _SymTable is a 2-dimensional numpy array such that:
#   if 'p' is the integer encoding of a position, 
#   we designate one of its symmetries 'r' as the representative of all its 8 symmetries
#   then  _SymTable[p] = [r,op]
#   where op is the index of a transform operation s.t. op(r) = p
# Additionally, all symmetries 'pk' of position 'p' will have the same
#   ... representative 'r' stored in _SymTable[pk,0]






# Encode a T-Board to an int
# When useSymmetry=True, encodes all symmetrically same boards to the same value.
def encode(tb : TicTacToeBoard, useSymmetry=True) -> int:
    N = _encodeBoardAsInteger(tb)
    if(useSymmetry is False):
        return N
    
    return tuple(lookUpSymTable(N))

# Decode a T-Board from an int
def decode(N : int) -> TicTacToeBoard:
    return _decodeBoardFromInteger(N)


# Perform a look-up of the SymTable
def lookUpSymTable(idx : int):
    global _SymTable
    if(_SymTable is None):
        loadSymmetryTable()
    try:
        return _SymTable[idx,:].copy()
    except IndexError:
        raise ValueError("Invalid index {} in lookUpSymTable()".format(idx))
        
# Return a copy of the SymTable
def getSymmetryTable():
    global _SymTable
    if(_SymTable is None):
        loadSymmetryTable()
    return _SymTable.copy()
        

    



# Getter method for the module-scoped variable _dataPathToSymTable.
# Also initializes its value when called for the first time.
def _getDataPathToSymTable():
    global _dataPathToSymTable
    
    if(_dataPathToSymTable is None):
        # Set it as the path to the file "SymTable.npy" 
        #    ... in the folder {project root}/data
        import Board
        temp = moduleDir(Board.__file__)  # gets the {project root 'dir'}
        _dataPathToSymTable = os.path.join(temp, 'data', 'SymTable.npy')
    
    return _dataPathToSymTable

        
# Calculate the symmetry table by generating all possible moves
def calcSymmetryTable():
    global _SymTable
    _SymTable = np.zeros(shape=(3**9,2), dtype=np.int32)
    _SymTable -= 1
    
    for N in range(3**9):
        if(_SymTable[N,0] != -1):
            continue
        
        b = _decodeVectorFromInteger(N)
        
        Bvecs = allVectorVariants(b)
        encodings = np.array([_encodeVectorAsInteger(b) for b in Bvecs])
        
        repEncoding = np.min(encodings)
        repVector = Bvecs[np.argmin(encodings)]
        
        for op in range(8):
            bt = transformVec(repVector, op)
            nbt = _encodeVectorAsInteger(bt)
            if(_SymTable[nbt,0]==-1):
                _SymTable[nbt,0] = repEncoding
                _SymTable[nbt,1] = op
    

# Save the symmetry table as a numpy file
def saveSymmetryTable():
    global _SymTable
    savePath = _getDataPathToSymTable()
    np.save(savePath, _SymTable, allow_pickle=False)

# Load the symmetry table from a numpy file
def loadSymmetryTable():
    global _SymTable
    loadPath = _getDataPathToSymTable()
    try:
        _SymTable = np.load(loadPath, allow_pickle=False)
    except OSError:
        msg = "File does not exist while trying to " +\
                "load the Symmetry Table from path: {}".format(loadPath)
        raise ValueError(msg)
    
    