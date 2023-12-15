
import os
import json

from Board import TicTacToeBoard
from TableBase import getAvailableTableBases
from Engine import TableBaseEngine, MiniMaxEngine
from  Helper import moduleDir


#                   Module-Scoped variable
##################################################################
_pathToSettingsFile = None

def _getPathToSettingsFile():
    global _pathToSettingsFile
    if(_pathToSettingsFile is None):
        dirName = moduleDir(__file__)
        _pathToSettingsFile = os.path.join(dirName, 'data', 'repl-settings-1.txt')
    return _pathToSettingsFile
##################################################################


def startGame():
    welcomeScreen()
    
    defaultSettings = {
                 "name1"   : "",
                 "name2"   : "",
                 "marker1" : "X",
                 "marker2" : "O",
                 "useTB"   : True
               }
    
    settings = tryToLoadSettings(default=defaultSettings)
    
    
    prevSettings = settings.copy()
    rsp = getSettings(settings, enableQuit=True, tryCnt=0)
    if(rsp == -1):
        exitMessage()
        return
    
    if(settings != prevSettings):
        tryToSaveSettings(settings)
    
    rsp = getPlayers(settings, enableQuit=True)
    if(rsp==-1):
        exitMessage()
        return
    else:
        (p1,p2) = rsp
    
    if('c' in (p1,p2)):
        if(settings['useTB']):
            eng = makeTableBaseEngine()
        else:
            eng = MiniMaxEngine()
        
    resp = input("\nPress ENTER to start the game ...")
    if(resp.strip().lower()=='q'):
        exitMessage()
        return
    
    tb = TicTacToeBoard()
    
    drawBoard(tb, settings, pre='\n')
    
    while(True):
        
        nextPlayer = (p1 if(tb.nextTurn==tb.Xmark) else p2)
        if(nextPlayer == 'u'):
            mv = getInputMove(tb, enableQuit=True)
            if(mv==-1):
                break
        else:
            _ = input("It's the Computer's turn. Press ENTER to continue ...")
            mv = eng.bestMove(tb, separateEqualsBy='random')
            print("\nThe computer makes a move at ({}, {})".format(mv//3+1, mv%3+1))
        
        tb.move(mv)
        
        drawBoard(tb, settings)
        
        if(tb.checkWin() != 0):
            if(nextPlayer==p1):
                winnerName = (settings['name1'] if(settings['name1']!='') else 'Player 1')
            else:
                winnerName = (settings['name2'] if(settings['name2']!='') else 'Player 2')
            print(winnerName, "wins!")
            break
        
        if(len(tb.possibleNextMoves()) == 0):
            print("It's a draw")
            break
        
    print("\nGAME OVER\n")
        
    
    
def welcomeScreen(enableQuit  = True):
    print("\nWELCOME TO TICTACTOE\n\n")
    print("Enter 'q' at any time to quit.")
    print()
        
def exitMessage():
    print()
    print("Exiting . . .")
    print()
    
    
def tryToLoadSettings(default):
    path = _getPathToSettingsFile()
    try:
        with open(path, "r") as jfile:
            ret = json.load(jfile)
    except (OSError, json.JSONDecodeError):
        return default
    else:
        return ret

def tryToSaveSettings(settings):
    path = _getPathToSettingsFile()
    try:
        with open(path, "w") as jfile:
            json.dump(settings, jfile)
    except OSError:
        pass
    

def makeTableBaseEngine():
    atb = getAvailableTableBases()
    tbname = list(atb.keys())[0]
    tbase = atb[tbname]
    eng = TableBaseEngine(tbase)
    return eng


def drawBoard(tb:TicTacToeBoard, settings, pre='\n', end='\n'):
    symbol = {
              0        :  " ",
              tb.Xmark :  settings['marker1'],
              tb.Ymark :  settings['marker2']
              }
    
    ret = pre
    
    dispName1 = (settings['name1'] if (settings['name1']!='') else "Player 1")
    dispName2 = (settings['name2'] if (settings['name2']!='') else "Player 2")
    toMoveLine = "Next Turn: "
    toMoveLine += (dispName1 if(tb.nextTurn==tb.Xmark) else dispName2)
    toMoveLine += " (" + (settings['marker1'] if (tb.nextTurn==tb.Xmark) else settings['marker2']) + ")"
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
    
    
def getSettings(settings, enableQuit = True, tryCnt = 0):
    
    while(True):
        tryCnt += 1
        
        if(tryCnt==1):
            print(" **** Default Settings ****")
        else:
            print(" **** Current Settings ****")
            
        print("Player 1's Name:", settings['name1'])
        print("Player 2's Name:", settings['name2'])
        print("Player 1's Marker:", settings['marker1'])
        print("Player 2's Marker:", settings['marker2'])
        print("Use a tablebase to speed up computer moves:", ('Yes' if settings['useTB'] else 'No'))
        print()
        resp = input("Change any of these settings? (Y to change): ")
        if(enableQuit is True and resp.strip().lower()=='q'):
            return -1
    
        
        if(resp.strip().lower() == 'y'):
            print()
            print("Press ENTER to leave any setting unchanged")
            print()
            
            resp = input("Player 1's Name (upto 20 characters): ").strip()
            if(enableQuit is True and resp.lower()=='q'):
                return -1
            if(resp!=''):
                settings['name1'] = resp[:20]
            
            resp = input("Player 2's Name (upto 20 characters): ").strip()
            if(enableQuit is True and resp.lower()=='q'):
                return -1
            if(resp!=''):
                settings['name2'] = resp[:20]
            
            resp = input("Player 1's Marker (1 character): ").strip()
            if(enableQuit is True and resp.lower()=='q'):
                return -1
            if(resp!=''):
                settings['marker1'] = resp[0]
            
            resp = input("Player 2's Marker (1 character): ").strip()
            if(enableQuit is True and resp.lower()=='q'):
                return -1
            if(resp!=''):
                settings['marker2'] = resp[0]
            
            resp = input("Should the computer use a tablebase to speed up its moves (Y/n): ").strip()
            if(enableQuit is True and resp.lower()=='q'):
                return -1
            settings['useTB'] = (resp.lower()!='n' and resp.lower()!='no')
            
            print()
            
        else:
            break
    
    return settings


def getPlayers(settings, enableQuit = True):
    dispName1 = settings['name1'] if settings['name1']!='' else "Player 1"
    dispName1 += ("'s") if (dispName1[-1].lower() != 's') else ("'")
        
    dispName2 = settings['name2'] if settings['name2']!='' else "Player 2"
    dispName2 += ("'s") if (dispName2[-1].lower() != 's') else ("'")
        
    cnt = 0
    while(True):
        cnt += 1
        
        r1 = input("\nWho makes " + dispName1 + " moves?: ('u' for user and 'c' for computer): ")
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
        r2 = input("\nWho makes " + dispName2 + " moves?: ('u' for user and 'c' for computer): ")
        r2 = r2.strip().lower()
        if(enableQuit is True and r2=='q'):
            return -1
        if(r2=='u' or r2=='c'):
            break
        else:
            print("Invalid Input. You must enter either 'u' or 'c'.")
            print("Try again ("+str(cnt)+")\n")
    
    print()
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
            print("\nInvalid Input. Expected format: row <SPACE> column")
            print("Try again({})\n\n".format(cnt))
            continue
        else:
            if(tb.board[ret]==0):
                return ret
            else:
                print("\n\nCo-ordinates are not empty. Try again({})\n".format(cnt))
                continue
            

if __name__ == '__main__':
    startGame()