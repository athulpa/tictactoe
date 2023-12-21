
#include <stdlib.h>
#include <stdio.h>

#define Xwins   (1)
#define Draw    (0)
#define Ywins   (-1)


typedef struct {
	int *B;
	int Xmark;
	int Ymark;
	int nextTurn;
} Tboard;


int move(Tboard *tb, int pos) {
	tb->B[pos] = tb->nextTurn;
	tb->nextTurn = ((tb->nextTurn == tb->Xmark) ? (tb->Ymark) : (tb->Xmark));
}

int undoMove(Tboard *tb, int pos) {
	tb->B[pos] = 0;
	tb->nextTurn = ((tb->nextTurn == tb->Xmark) ? (tb->Ymark) : (tb->Xmark));
}


// Can be called from python module. Arguments passed must be of python type: "bytes"
// The first argument must be a T-board, construct it using "bytes(tb.board)" where tb is a python TicTacToeBoard object
int checkWin(int* B) {
	
	// First Row
	if(B[0] != 0   &&  B[1]==B[0]  &&  B[2]==B[0])
		return 1;
	
	//Second Row
	if(B[3] != 0   &&  B[4]==B[3]  &&  B[5]==B[3])
		return 1;
	
	// Third Row
	if(B[6] != 0   &&  B[7]==B[6]  &&  B[8]==B[6])
		return 1;
	
	// First Col
	if(B[0] != 0   &&  B[3]==B[0]  &&  B[6]==B[0])
		return 1;
	
	//Second Col
	if(B[1] != 0   &&  B[4]==B[1]  &&  B[7]==B[1])
		return 1;
	
	// Third Col
	if(B[2] != 0   &&  B[5]==B[2]  &&  B[8]==B[2])
		return 1;
	
	// Leading diag
	if(B[0] != 0   &&  B[4]==B[0]  &&  B[8]==B[0])
		return 1;
	
	// Alternate diag
	if(B[2] != 0   &&  B[4]==B[2]  &&  B[6]==B[2])
		return 1;
	
	return 0;
}
	
	
int minimax_AlphaBetaPruning(Tboard *tb, int XgotDraw, int YgotDraw, int *cnt) {
	(*cnt)++;
	
	int atLeastOneMove = 0;
	// For all possible moves
	for(int mv=0; mv<9; mv++) {
		
		// Skip move if it's already played
		if(tb->B[mv] != 0)
			continue;
		
		atLeastOneMove = 1;
		
		move(tb, mv);
		
		if(checkWin(tb->B)) {
			undoMove(tb, mv);
			return (  ((tb->nextTurn) == (tb->Xmark)) ? (Xwins) : (Ywins)  );
		}
		
		int Z = minimax_AlphaBetaPruning(tb, XgotDraw, YgotDraw, cnt);
		
		undoMove(tb,mv);
		
		// What to do each move if optimizing on X's side
		if((tb->nextTurn) == (tb->Xmark)) {
			if(Z == Xwins)
				return Xwins;
			else if(Z == Draw) {
				if(YgotDraw)
					return Draw;
				XgotDraw = 1;
			}
		}
		
		
		// What to do each move if optimizing on Y's side
		else {
			if(Z == Ywins)
				return Ywins;
			else if(Z == Draw) {
				if(XgotDraw)
					return Draw;
				YgotDraw = 1;
			}
		}
	
	}
	
	if(!atLeastOneMove)
		return Draw;
	
	// What to do after parsing all possible moves, if optimizing on X's side
	if((tb->nextTurn) == (tb->Xmark))
		return (XgotDraw ? Draw : Ywins);
	
	// What to do after parsing all possible moves, if optimizing on Y's side
	else
		return (YgotDraw ? Draw : Xwins);
		
}

int minimax(Tboard *tb, int *cnt) {
	(*cnt)++;
	
	int foundDraw = 0;
	int atLeastOneMove = 0;
	// For all possible moves
	for(int mv=0; mv<9; mv++) {
		
		// Skip move if it's already played
		if(tb->B[mv] != 0)
			continue;
		
		atLeastOneMove = 1;
		
		move(tb, mv);
		
		if(checkWin(tb->B)) {
			undoMove(tb, mv);
			return (  ((tb->nextTurn) == (tb->Xmark)) ? (Xwins) : (Ywins)  );
		}
		
		int Z = minimax(tb, cnt);
		
		undoMove(tb,mv);
		
		if(Z==0)
			foundDraw = 1;
		
		
		// What to do each move if optimizing on X's side
		if((tb->nextTurn) == (tb->Xmark)) {
			if(Z == Xwins)
				return Xwins;
		}
		
		// What to do each move if optimizing on Y's side
		else {
			if(Z == Ywins)
				return Ywins;
		}
	}
	
	if(!atLeastOneMove)
		return Draw;
	
	if(foundDraw)
		return Draw;
	
	// What to do after parsing all possible moves, if optimizing on X's side
	else if((tb->nextTurn) == (tb->Xmark))
		return Ywins;
	
	// What to do after parsing all possible moves, if optimizing on Y's side
	else
		return Xwins;
		
}

// Called from python module. Arguments passed must be of python types: "bytes", "int", "int", "int", "bytes"
// The first argument must be a T-board, construct it using "bytes(tb.board)" where tb is a python TicTacToeBoard object
int run_Minimax(unsigned char* brd, int nextTurn, int Xmark,  int Ymark, unsigned char *count) {
	
	Tboard *tb = (Tboard *) malloc(sizeof(Tboard));
	
	tb->Xmark     =  Xmark;
	tb->Ymark     =  Ymark;
	tb->nextTurn  =  nextTurn;
	
	tb->B = (int *) calloc(9,sizeof(int));
	for(int i=0; i<9; i++)
		tb->B[i] = (int) brd[i];
	
	int *cnt = (int *) malloc(sizeof(int));
	*cnt = 0;
	
	int ret = minimax(tb, cnt);
	
	(*count) = (unsigned char) (*cnt/256);
	count++;
	(*count) = (unsigned char) (*cnt%256);
	
	free(tb->B);
	free(tb);
	free(cnt);
	
	return ret;
}

// Called from python module. Arguments passed must be of python types: "bytes", "int", "int", "int", "bytes"
// The first argument must be a T-board, construct it using "bytes(tb.board)" where tb is a python TicTacToeBoard object
int run_Minimax_Pruning(unsigned char* brd, int nextTurn, int Xmark,  int Ymark, unsigned char *count) {
	
	Tboard *tb = (Tboard *) malloc(sizeof(Tboard));
	
	tb->Xmark     =  Xmark;
	tb->Ymark     =  Ymark;
	tb->nextTurn  =  nextTurn;
	
	tb->B = (int *) calloc(9,sizeof(int));
	for(int i=0; i<9; i++)
		tb->B[i] = (int) brd[i];
	
	int *cnt = (int *) malloc(sizeof(int));
	*cnt = 0;
	
	int ret = minimax_AlphaBetaPruning(tb, 0, 0, cnt);
	
	(*count) = (unsigned char) (*cnt/256);
	count++;
	(*count) = (unsigned char) (*cnt%256);
	
	free(tb->B);
	free(tb);
	free(cnt);
	
	return ret;
}

