
from Board import TicTacToeBoard


#      Fns to Transform the T-Board object
#################################################
def flipud(tb : TicTacToeBoard):
    ret = TicTacToeBoard(copyFrom=tb)
    ret.board = flipud_Vec(tb.board)
    return ret  

def fliplr(tb : TicTacToeBoard):
    ret = TicTacToeBoard(copyFrom=tb)
    ret.board = fliplr_Vec(tb.board)
    return ret

def rotateLeft(tb : TicTacToeBoard):
    ret = TicTacToeBoard(copyFrom=tb)    
    ret.board = rotateLeft_Vec((tb.board))
    return ret

def rotateRight(tb : TicTacToeBoard):
    ret = TicTacToeBoard(copyFrom=tb)
    ret.board = rotateRight_Vec(tb.board)
    return ret

def rotate180(tb : TicTacToeBoard):
    ret = TicTacToeBoard(copyFrom=tb)
    ret.board = rotate180_Vec(tb.board)
    return ret
#################################################




#       Fns to Transform the Board Vector
#################################################
def flipud_Vec(vec):
    ret = vec.copy()
    ret[0:3] = vec[6:9]
    ret[6:9] = vec[0:3]
    return ret


def fliplr_Vec(vec):
    ret = vec.copy()
    ret[0:9:3] = vec[2:9:3]
    ret[2:9:3] = vec[0:9:3]
    return ret


def rotateLeft_Vec(vec):
    ret = vec.copy()
    
    r = ret; t = vec
    r[0] = t[2]; r[1] = t[5]; r[2] = t[8];
    r[3] = t[1]; r[4] = t[4]; r[5] = t[7];
    r[6] = t[0]; r[7] = t[3]; r[8] = t[6];

    return ret


def rotateRight_Vec(vec):
    ret = vec.copy()
    
    r = ret; t = vec
    r[0] = t[6]; r[1] = t[3]; r[2] = t[0];
    r[3] = t[7]; r[4] = t[4]; r[5] = t[1];
    r[6] = t[8]; r[7] = t[5]; r[8] = t[2];

    return ret

def rotate180_Vec(vec):
    ret = vec.copy()
    
    ret[0:3] = vec[8:5:-1]
    ret[3:6] = vec[5:2:-1]
    ret[6:9] = vec[2::-1]
    return ret
#################################################

