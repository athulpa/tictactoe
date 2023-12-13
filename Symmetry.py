

from Board import TicTacToeBoard
from FlipRotate import fliplr, rotate180, rotateLeft, rotateRight
from FlipRotate import fliplr_Vec, rotate180_Vec, rotateLeft_Vec, rotateRight_Vec



#        Operations of the D8 group
###########################################
#    INDEX - OPERATION
#       0  -  Self
#       1  -  Rotate Right (clockwise)
#       2  -  Rotate Upside-Down
#       3  -  Rotate Left (anti-clockwise)
#       4  -  FlipLR (left-to-right)
#       5  -  FlipLR and Rotate Right (clockwise)
#       6  -  FlipLR and Rotate Upside-Down
#       7  -  FlipLR and Rotate Left (anti-clockwise)


# A list mapping each operation(0-7) to it's inverse.
# Applying  operation 'op' and then _inverseOperation[op] will result in no change.
_inverseOperation = [0, 3, 2, 1, 4, 5, 6, 7]


# _newIndex[op][i], with (0<=op<8) and (0<=i<9), tells the new index of the ...
#   ... cell at 'i' after its board is modified by the operation indexed 'op'
_newIndex = [
            [0,1,2, 3,4,5, 6,7,8],
            [2,5,8, 1,4,7, 0,3,6],
            [8,7,6, 5,4,3, 2,1,0],
            [6,3,0, 7,4,1, 8,5,2],
            [2,1,0, 5,4,3, 8,7,6],
            [8,5,2, 7,4,1, 6,3,0],
            [6,7,8, 3,4,5, 0,1,2],
            [0,3,6, 1,4,7, 2,5,8]
           ]


# Getter method for the module-scoped '_inverseOperation'
def inverseOperation(opIdx):
    try:
        return _inverseOperation[opIdx]
    except (IndexError,ValueError,TypeError):
        msg = "Invalid call to inverseOperation({}).".format(opIdx) + \
                "Index must be in range(0,8)"
        raise ValueError(msg)
        

# Returns the new index of a cell if one of the D8 operations were ...
#   ... applied to the board
def newIndex(idx, opIdx):
    try:
        return _newIndex[opIdx][idx]
    except (IndexError, ValueError, TypeError) as e:
        msg = "Invalid call to newIndex({}, {}).".format(idx,opIdx) + \
                "Index must bean int in [0,8] and opIdx must be an int in [0,7]"
        raise ValueError(msg) from e

# Returns the old index of a cell before one of the D8 operations were ...
#   ... applied to the board
def oldIndex(idx, opIdx):
    try:
        opIdx = _inverseOperation[opIdx]
        return _newIndex[opIdx][idx]
    except (IndexError, ValueError, TypeError) as e:
        msg = "Invalid call to oldIndex({}, {}).".format(idx,opIdx) + \
                "Index must bean int in [0,8] and opIdx must be an int in [0,7]"
        raise ValueError(msg) from e
 
        
 
        
# Applies any of the operators of the D8 group to the input T-Board.
# Returns a new T-Board.
def transformBoard(tb : TicTacToeBoard, opIdx : int):
    if(opIdx==0):
        return TicTacToeBoard(copyFrom=tb)
    elif(opIdx==1):
        return  rotateRight(tb)
    elif(opIdx==2):
        return rotate180(tb)
    elif(opIdx==3):
        return rotateLeft(tb)
    elif(opIdx==4):
        return fliplr(tb)
    elif(opIdx==5):
        return rotateRight(fliplr(tb))
    elif(opIdx==6):
        return rotate180(fliplr(tb))
    elif(opIdx==7):
        return rotateLeft(fliplr(tb))
    else:
        msg = "Invalid Operation Index in call to transformBoard({})".format(opIdx)
        raise ValueError(msg)
    
    
# Applies any of the operators of the D8 group to the input.
# Returns a new board-vector.
def transformVec(vec, opIdx : int):
    if(opIdx==0):
        return vec.copy()
    elif(opIdx==1):
        return  rotateRight_Vec(vec)
    elif(opIdx==2):
        return rotate180_Vec(vec)
    elif(opIdx==3):
        return rotateLeft_Vec(vec)
    elif(opIdx==4):
        return fliplr_Vec(vec)
    elif(opIdx==5):
        return rotateRight_Vec(fliplr_Vec(vec))
    elif(opIdx==6):
        return rotate180_Vec(fliplr_Vec(vec))
    elif(opIdx==7):
        return rotateLeft_Vec(fliplr_Vec(vec))
    else:
        msg = "Invalid Operation Index in call to transformVec({})".format(opIdx)
        raise ValueError(msg)
    
        
# Return all symmetric variants of the input T-Board.
# Returns a list of T-Boards after applying each operation in order of its op-index.
def allBoardVariants(tb : TicTacToeBoard):
    return [transformBoard(tb, op) for op in range(8)]

# Return all symmetric variants of the input board-vector
# Returns a list of board-vectors after applying each operation in order of its op-index.
def allVectorVariants(vec):
    return  [transformVec(vec, op) for op in range(8)]


# Return all unique symmetric variants of the input T-Board.
def allUniqueBoardVariants(tb : TicTacToeBoard):
    ret = list()
    for b in allBoardVariants(tb):
        if(b not in ret):
            ret.append(b)
    return ret
            
# Return all unique symmetric variants of the input board-vector
def allUniqueVectorVariants(tb : TicTacToeBoard):
    ret = list()
    for b in allVectorVariants(tb):
        if(b not in ret):
            ret.append(b)
    return ret