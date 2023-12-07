

from Board import TicTacToeBoard
from Engine import TicTacToeEngine

def startSimpleGame():
    eng = TicTacToeEngine()
    tb = TicTacToeBoard()
    
    p1,p2 = welcomeScreen()

    print("\n\nLET'S BEGIN!\n")
    
    drawBoard(tb)
    
    while(True):
        
        nextPlayer = (p1 if(tb.nextTurn==tb.Xmark) else p2)
        if(nextPlayer == 'u'):
            mv = getInputMove(tb)
            if(mv==-1):
                break
        else:
            _ = input("Computer's turn, press ENTER to continue ...")
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



def welcomeScreen():
    print("\nWELCOME TO TICTACTOE\n\n")
    print("The first player plays 'X' and moves first.\nThe second player plays 'O'.")
    
    cnt = 0
    while(True):
        cnt += 1
        r1 = input("\nWho plays first? ('u' for user and 'c' for computer): ")
        r1 = r1.strip().lower()
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
        if(r2 == 'u' or r2=='c'):
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
        
        inp = input("Co-ordinates for the next move? ")
        if(enableQuit is True and inp.strip().lower()=='q'):
            return -1
        try:
            nums = [int(i) for i in inp.strip().split()]
            assert ((len(nums)==2) and (nums[0] in range(1,4)) and (nums[1] in range(1,4)))
            ret = 3*(nums[0]-1) + (nums[1]-1)
        except (AssertionError, ValueError, TypeError):
            print("\n\nInvalid Input. Try again({})\n".format(cnt))
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