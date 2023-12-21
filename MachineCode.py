
import ctypes
import platform
import os

from Helper import extendRootPath


#                             Custom Exceptions
###############################################################################

# Thrown if the .dll/.so file is not found
class MachineCodeMissingError(FileNotFoundError):
    pass

# Thrown if the .dll/.so file can't be loaded by the python process
class MachineCodeLoadingError(OSError):
    pass

# Thrown if machine code fuction encounters a runtime error
# For eg: C pointer error or segfault
class MachineCodeRuntimeError(RuntimeError):
    pass
###############################################################################




#       Module-Scope Variables (a.k.a globals)
#########################################################
_platform = None

_minimax_DLL_FileName = None

_minimax_DLL = None
#########################################################

    
def _getPlatform():
    global _platform
    
    if(_platform is None):
        #_paltform = os.name
        #_platform = sys.platform
        _platform = platform.system()
        #_platform = platform.platform()
        
    return _platform

def _getMinimax_DLL_FileName():
    global _minimax_DLL_FileName
    if(_minimax_DLL_FileName is None):
        pf = _getPlatform()
        if(pf.lower() == 'windows'):
            _minimax_DLL_FileName = extendRootPath("cforspeed", "minimax.dll")
        elif(pf.lower() == 'linux'):
            _minimax_DLL_FileName = extendRootPath("cforspeed", "minimax.so")
        else:         # Leave it as None if _platform is not an expected one
            _minimax_DLL_FileName = None 
    return _minimax_DLL_FileName
    
def _get_Minimax_CDLL():
    global _minimax_DLL
    if(_minimax_DLL is None):
        fname = _getMinimax_DLL_FileName()
        if(fname is None):
            msg = "Could not recognize the library file for the current"  + \
                   "platform: \'{}'.\nYou can specify the path to ".format(_getPlatform()) + \
                    "a compatible library file by setting the variable " + \
                    "'_minimax_DLL_FileName' in MachineCode.py"
            raise MachineCodeMissingError(msg)
        
        try:
            mdl = ctypes.CDLL(fname)
        except FileNotFoundError:
            msg = "The required shared library file '{}' ".format(os.path.basename(fname)) + \
                    "was not found in {}.".format(os.path.dirname(fname)) + \
                    "\nCompile it from 'minimax.c' using an appropriate C compiler."
            raise MachineCodeMissingError(msg)
        except OSError as e:
            msg = "The shared library file '{}' is not compatible.".format(fname) + \
                    "\nRecompile it from 'minimax.c' using an appropriate C compiler."
            raise MachineCodeLoadingError(msg) from e
            
    return mdl




#               Functions that call machine code
###############################################################################
# Run the minimax algorithm, compiled to native machine code.
# Approx. 1000X faster than the python version of minimax.
def run_minimax(tb, pruning=True):
    mdl = _get_Minimax_CDLL()
    
    count = bytes([0,0])
    brd = bytes(tb.board)
    
    if(pruning is True):
        try:
            Z = mdl.run_Minimax_Pruning(brd, tb.nextTurn, tb.Xmark, tb.Ymark, count)
        except (OSError, RuntimeError) as e:
            fname = _getMinimax_DLL_FileName()
            msg = "Error while running machine code from '{}' ".format(os.path.basename(fname)) + \
                  "in {}.\n Check the source code, compiler options ".format(os.path.dirname(fname)) + \
                  "and the bit-version of python.exe, then recompile it from minimax.c"
            raise MachineCodeRuntimeError(msg) from e
    else:
        try:
            Z = mdl.run_Minimax(brd, tb.nextTurn, tb.Xmark, tb.Ymark, count)
        except (OSError, RuntimeError) as e:
            fname = _getMinimax_DLL_FileName()
            msg = "Error while running machine code from '{}' ".format(os.path.basename(fname)) + \
                  "in {}.\n Check the source code, compiler options ".format(os.path.dirname(fname)) + \
                  "and the bit-version of python.exe, then recompile it from minimax.c"
            raise MachineCodeRuntimeError(msg) from e
    cnt = count[1]*256+count[0]
    
    return Z,cnt


# Run the checkWin algorithm, written in C code and compiled
def checkWin(tb):
    mdl = _get_Minimax_CDLL()
    try:
        return mdl.checkWin(bytes(tb.board))
    except (OSError, RuntimeError) as e:
        fname = _getMinimax_DLL_FileName()
        msg = "Error while running machine code from '{}' ".format(os.path.basename(fname)) + \
              "in {}.\n Check the source code, compiler options ".format(os.path.dirname(fname)) + \
              "and the bit-version of python.exe, then recompile it from minimax.c"
        raise MachineCodeRuntimeError(msg) from e
###############################################################################