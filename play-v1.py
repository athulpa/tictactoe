

from Board import TicTacToeBoard
from Engine import MiniMaxEngine
from Engine import TableBaseEngine
from TableBase import getAvailableTableBases

def startSimpleGame():
    #eng = MiniMaxEngine()
    eng = makeTableBaseEngine()
    
    tb = TicTacToeBoard()
    
    rsp = welcomeScreen()
    if(rsp==-1):
        print("\nExiting ...\n")
        return
    else:
        (p1,p2) = rsp

    print("\n\nLET'S BEGIN!\n")
    
    drawBoard(tb)
    
    while(True):
        
        nextPlayer = (p1 if(tb.nextTurn==tb.Xmark) else p2)
        if(nextPlayer == 'u'):
            mv = getInputMove(tb)
            if(mv==-1):
                break
        else:
            _ = input("It's the Computer's turn. Press ENTER to continue ...")
            mv = eng.bestMove(tb, separateEqualsBy='random')
            print("\nThe computer makes a move at ({}, {})".format(mv//3+1, mv%3+1))
        
        tb.move(mv)
        
        drawBoard(tb)
        
        if(tb.checkWin() != 0):
            print("Player {} wins!".format('1' if(nextPlayer==p1) else '2'))
            break
        
        if(len(tb.possibleNextMoves()) == 0):
            print("It's a draw")
            break
        
    print("\nGAME OVER\n")


def makeTableBaseEngine():
    atb = getAvailableTableBases()
    tbname = list(atb.keys())[0]
    tbase = atb[tbname]
    eng = TableBaseEngine(tbase)
    return eng

def welcomeScreen(enableQuit=True):
    print("\nWELCOME TO TICTACTOE\n\n")
    print("PLAYER RULES")
    print("The first player plays 'X' and moves first.\nThe second player plays 'O'.")
    print()
    print()
    print("BOARD RULES")
    print("The game will be played on a 3x3 board.")
    print("Each cell has numbered co-ordinates of the form (row number, column number).")
    print("Rows are numbered 1-3 from top to bottom; columns are numbered 1-3 from left to right.")
    print("For instance, (1,1) is the top-left cell and (2,3) is the middle-right cell.")
    print()
    print()
    print("To quit, type 'q' when asked for any input.")
    print()
    print()
    _ = input("Press ENTER to continue ...")
    print()
    
    cnt = 0
    while(True):
        cnt += 1
        r1 = input("\nWho plays first? ('u' for user and 'c' for computer): ")
        r1 = r1.strip().lower()
        if(enableQuit is True and r1=='q'):
            return -1
        if(r1 == 'u' or r1=='c'):
            break
        else:
            print("Invalid Input. You must enter either 'u' or 'c'.")
            print("Try again ("+str(cnt)+")\n")
            
    cnt = 0
    while(True):
        cnt += 1
        r2 = input("\nWho plays second? ('u' for user and 'c' for computer): ")
        r2 = r2.strip().lower()
        if(enableQuit is True and r2=='q'):
            return -1
        if(r2=='u' or r2=='c'):
            break
        else:
            print("Invalid Input. You must enter either 'u' or 'c'.")
            print("Try again ("+str(cnt)+")\n")
            
    return r1,r2


# Gets the next move from the user
# If quit is enabled, returns -1 if the user enters 'q' to signal a game over
def getInputMove(tb, enableQuit=True):
    cnt = 0
    
    while(True):
        cnt += 1
        
        inp = input("Co-ordinates for the next move?: ")
        if(enableQuit is True and inp.strip().lower()=='q'):
            return -1
        try:
            nums = [int(i) for i in inp.strip().split()]
            assert ((len(nums)==2) and (nums[0] in range(1,4)) and (nums[1] in range(1,4)))
            ret = 3*(nums[0]-1) + (nums[1]-1)
        except (AssertionError, ValueError, TypeError):
            print("\nInvalid Input. Expected format: row-index <SPACE> column-index")
            print("Try again({})\n\n".format(cnt))
            continue
        else:
            if(tb.board[ret]==0):
                return ret
            else:
                print("\n\nCo-ordinates are not empty. Try again({})\n".format(cnt))
                continue
            

def drawBoard(tb:TicTacToeBoard, Xchar='X', Ychar='O', pre='\n', end='\n'):
    symbol = {
              0        :  " ",
              tb.Xmark :  Xchar,
              tb.Ymark :  Ychar
              }
    
    ret = pre
    
    toMoveLine = "Next: "
    toMoveLine += (Xchar if(tb.nextTurn==tb.Xmark) else Ychar)
    toMoveLine +=  '\n'
    
    for i in range(3):
        for j in range(3):
            ret += " " + symbol[tb.board[3*i+j]] + " |"
        if(i!=2):
            ret = ret[:-1] + "\n" + "-"*11 + "\n"
        else:
            ret = ret[:-1] + '\n'
    
    ret += '\n' + toMoveLine
    ret += end
    print(ret)
    
if __name__=='__main__':
    startSimpleGame()
    
