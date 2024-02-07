#!/usr/bin/env python3
from FourConnect import * # See the FourConnect.py file
import csv
import math
from random import shuffle
import time


GAMETREE_PLAYER    = 2
MYOPIC_PLAYER = 1

class GameTreePlayer:    
    
    def _init_(self):
        pass
    
    def winning(self,board, piece):
        # Check horizontal locations for win
        for c in range(7-3):
            for r in range(6):
                if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                    return True

        # Check vertical locations for win
        for c in range(7):
            for r in range(6-3):
                if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                    return True

        # Check positively sloped diaganols
        for c in range(7-3):
            for r in range(6-3):
                if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                    return True

        # Check negatively sloped diaganols
        for c in range(7-3):
            for r in range(3, 6):
                if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                    return True

    def evaluate(self,window, piece = GAMETREE_PLAYER):
        score = 0
        opp_piece = MYOPIC_PLAYER
        if piece == MYOPIC_PLAYER:
            opp_piece = GAMETREE_PLAYER

        if window.count(piece) == 4:
            score += 1000000000
        elif window.count(piece) == 3 and window.count(0) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(0) == 2:
            score += 2
            
        if window.count(opp_piece) == 4:
            score -= 10000000000
        if window.count(opp_piece) == 3 and window.count(0) == 1:
            score -= 4

        return score

    def evaluate2(self, window, piece=GAMETREE_PLAYER):
        score = 0
        opp_piece = MYOPIC_PLAYER if piece == GAMETREE_PLAYER else GAMETREE_PLAYER
    
        # Count player's pieces in the window
        player_count = window.count(piece)
        # Count opponent's pieces in the window
        opp_count = window.count(opp_piece)
        # Count empty spaces in the window
        empty_count = window.count(0)
    
        # Reward for having more pieces in the window
        score += player_count * 1000000
        # Penalize the opponent for having more pieces in the window
        score -= opp_count * 10000
        # Additional reward for having empty spaces to potentially complete a line
        score += empty_count * 100
    
        return score

    
    def evaluate3(self, window, piece=GAMETREE_PLAYER):
        score = 0
        opp_piece = MYOPIC_PLAYER if piece == GAMETREE_PLAYER else GAMETREE_PLAYER

        if window.count(piece) == 4:
            return 2000
        elif window.count(opp_piece) == 4:
            return -2000
        else:
            return 0
    

        


    def utilityValue(self,board, piece = GAMETREE_PLAYER):
        score = 0

        

        ## Score Horizontal
        for r in range(6):
            
            row_array = []
            for j in range(len(board[r])):
                row_array.append(int(board[r][j]))
            for c in range(7-3):
                window = row_array[c:c+4]
                score += self.evaluate(window, piece)

        ## Score Vertical
        for c in range(7):
            
            col_array = []
            for row in board:
                col_array.append(int(row[c]))
            for r in range(6-3):
                window = col_array[r:r+4]
                score += self.evaluate(window, piece)

        ## Score posiive sloped diagonal
        for r in range(6-3):
            for c in range(7-3):
                window = [board[r+i][c+i] for i in range(4)]
                score += self.evaluate(window, piece)

        for r in range(6-3):
            for c in range(7-3):
                window = [board[r+3-i][c+i] for i in range(4)]
                score += self.evaluate(window, piece)

        return score

    def is_terminal(self,currentState):
        
        valid = False
        for c in range(7):
            if currentState[0][c] == 0:
                valid = True
                break
    
        if valid == False:                                  
            return True
        elif self.winning(currentState, GAMETREE_PLAYER):
            return True
        elif self.winning(currentState, MYOPIC_PLAYER):
            return True
        else:
            return False

    def valid_locations(self,currentState):
        valid_locations = []
        for c in range(7):
            if currentState[0][c] == 0:
                valid_locations.append(c)

        return valid_locations

    def makeMove(self, board, col, player):
       
        tempBoard = [row[:] for row in board]
        for row in range(5, -1, -1):
            if tempBoard[row][col] == 0:
                tempBoard[row][col] = player
                return tempBoard, row, col

        
        return board, -1, -1


    def move_order_heuristic(self, board, move, player):
        # Evaluate the heuristic value of the resulting board after making the move
        tempBoard, _, _ = self.makeMove(board, move, player)

        # Count potential connections for the AI player
        ai_connections = self.evaluate_connections(tempBoard, GAMETREE_PLAYER)

        # Count potential connections for the human player
        human_connections = self.evaluate_connections(tempBoard, MYOPIC_PLAYER)

        # The heuristic value is the difference between AI and human potential connections
        return ai_connections - human_connections

    def evaluate_connections(self, board, player):
        connections = 0

        # Evaluate horizontal connections
        for r in range(6):
            for c in range(7 - 3):
                window = [board[r][c+i] for i in range(4)]
                connections += self.count_connections(window, player)

        # Evaluate vertical connections
        for c in range(7):
            for r in range(6 - 3):
                window = [board[r+i][c] for i in range(4)]
                connections += self.count_connections(window, player)

        # Evaluate positively sloped diagonal connections
        for r in range(6 - 3):
            for c in range(7 - 3):
                window = [board[r+i][c+i] for i in range(4)]
                connections += self.count_connections(window, player)

        # Evaluate negatively sloped diagonal connections
        for r in range(3, 6):
            for c in range(7 - 3):
                window = [board[r-i][c+i] for i in range(4)]
                connections += self.count_connections(window, player)

        return connections

    def count_connections(self, window, player):
        ai_count = window.count(GAMETREE_PLAYER)
        human_count = window.count(MYOPIC_PLAYER)

        # A connection is possible if there are no opponent pieces in the window
        if (player == GAMETREE_PLAYER and human_count == 0) or (player == MYOPIC_PLAYER and ai_count == 0):
            return ai_count + human_count

        return 0

    


    def MiniMaxAlphaBetaHEU(self, board, depth, player):
        validMoves = self.valid_locations(board)
        shuffle(validMoves)  # Randomize move order for initial exploration

        # Order moves based on material gain heuristic
        ordered_moves = sorted(validMoves, key=lambda move: self.move_order_heuristic(board, move, player), reverse=True)

        bestMove = ordered_moves[0]
        bestScore = float("-inf")

        alpha = float("-inf")
        beta = float("inf")

        if player == GAMETREE_PLAYER:
            opponent = MYOPIC_PLAYER
        else:
            opponent = GAMETREE_PLAYER

        for move in ordered_moves:
            tempBoard = self.makeMove(board, move, player)[0]
            boardScore = self.minimizeBeta(tempBoard, depth - 1, alpha, beta, player, opponent)
            if boardScore > bestScore:
                bestScore = boardScore
                bestMove = move

        return bestMove



    
    def MiniMaxAlphaBeta(self, board, depth, player):
        # get array of possible moves 
        validMoves = self.valid_locations(board)
        shuffle(validMoves)
        bestMove  = validMoves[0]
        bestScore = float("-inf")

        # initial alpha & beta values for alpha-beta pruning
        alpha = float("-inf")
        beta = float("inf")

        if player == GAMETREE_PLAYER: opponent = MYOPIC_PLAYER
        else: opponent = GAMETREE_PLAYER
    
        # go through all of those boards
        for move in validMoves:
            # create new board from move
            tempBoard = self.makeMove(board, move, player)[0]
            # call min on that new board
            boardScore = self.minimizeBeta(tempBoard, depth - 1, alpha, beta, player, opponent)
            if boardScore > bestScore:
                bestScore = boardScore
                bestMove = move
        return bestMove

    def minimizeBeta(self,board, depth, a, b, player, opponent):
        validMoves = []
        for col in range(7):
            
            isValid = False
            for row in range(6):
                if board[row][col] == 0:
                    isValid = True
                    
            if isValid:
                
                temp = self.makeMove(board, col, player)[2]
                validMoves.append(temp)

        if depth == 0 or len(validMoves) == 0 or self.is_terminal(board):
            return self.utilityValue(board, player)
        
        validMoves = self.valid_locations(board) 
        beta = b
        
       
        for move in validMoves:
            boardScore = float("inf")
            
            if a < beta:
                tempBoard = self.makeMove(board, move, opponent)[0]
                boardScore = self.maximizeAlpha(tempBoard, depth - 1, a, beta, player, opponent)

            if boardScore < beta:
                beta = boardScore
        return beta

    def maximizeAlpha(self,board, depth, a, b, player, opponent):
        validMoves = []
        for col in range(7):
            
            
            isValid = False
            if board[0][col] == 0:
                isValid = True
                    
            if isValid:
               
                temp = self.makeMove(board, col, player)[2]
                validMoves.append(temp)
      
        if depth == 0 or len(validMoves) == 0 or self.is_terminal(board):
            return self.utilityValue(board, player)

        alpha = a        
    
        for move in validMoves:
            boardScore = float("-inf")
            if alpha < b:
                tempBoard = self.makeMove(board, move, player)[0]
                boardScore = self.minimizeBeta(tempBoard, depth - 1, alpha, b, player, opponent)

            if boardScore > alpha:
                alpha = boardScore
        return alpha
                
                
    def FindBestAction(self,currentState):
        """
        Modify this function to search the GameTree instead of getting input from the keyboard.
        The currentState of the game is passed to the function.
        currentState[0][0] refers to the top-left corner position.
        currentState[5][6] refers to the bottom-right corner position.
        Action refers to the column in which you decide to put your coin. The actions (and columns) are numbered from left to right.
        Action 0 is refers to the left-most column and action 6 refers to the right-most column.
        """
        
        
    
        
        bestAction = self.MiniMaxAlphaBetaHEU(currentState,3,GAMETREE_PLAYER)  
        return bestAction
        


def LoadTestcaseState():
    testcaseState = list()

    with open('testcase.csv', 'r') as read_obj: 
        csvReader = csv.reader(read_obj)
        for csvRow in csvReader:
            row = [int(r) for r in csvRow]
            testcaseState.append(row)

    return testcaseState


#def PlayGame():
#    fourConnect = FourConnect()
#    # fourConnect.PrintGameState()
#    gameTree = GameTreePlayer()
#    
#    move=0
#    while move<42: #At most 42 moves are possible
#        if move%2 == 0: #Myopic player always moves first
#            fourConnect.MyopicPlayerAction()
#        else:
#            currentState = fourConnect.GetCurrentState()
#            gameTreeAction = gameTree.FindBestAction(currentState)
#            fourConnect.GameTreePlayerAction(gameTreeAction)
#        # fourConnect.PrintGameState()
#        move += 1
#        if fourConnect.winner!=None:
#            break
#    
#    """
#    You can add your code here to count the number of wins average number of moves etc.
#    You can modify the PlayGame() function to play multiple games if required.
#    """
#    if fourConnect.winner==None:
#        print("Game is drawn.")
#    else:
#        print("Winner : Player {0}      ".format(fourConnect.winner))
#    print("Moves : {0}".format(move))
#    
#    return move,fourConnect.winner 
#    
#
def RunTestCase():
    """
    This procedure reads the state in testcase.csv file and start the game.
    Player 2 moves first. Player 2 must win in 5 moves to pass the testcase; Otherwise, the program fails to pass the testcase.
    """
    
    fourConnect = FourConnect()
    gameTree = GameTreePlayer()
    testcaseState = LoadTestcaseState()
    fourConnect.SetCurrentState(testcaseState)
    fourConnect.PrintGameState()

    move=0
    while move<5: #Player 2 must win in 5 moves
        if move%2 == 1: 
            fourConnect.MyopicPlayerAction()
        else:
            currentState = fourConnect.GetCurrentState()
            gameTreeAction = gameTree.FindBestAction(currentState)
            fourConnect.GameTreePlayerAction(gameTreeAction)
        fourConnect.PrintGameState()
        move += 1
        if fourConnect.winner!=None:
            break
    
    print("Roll no : 2020B1A72102G") #Put your roll number here
    
    if fourConnect.winner==2:
        print("Player 2 has won. Testcase passed.")
    else:
        print("Player 2 could not win in 5 moves. Testcase failed.")
    print("Moves : {0}".format(move))
    

def main():
    
    #
    #total_moves = 0
    #ai_wins = 0
    #start_time = time.time()

    #for _ in range(50):
    #    moves, winner = PlayGame()

    #    total_moves += moves

    #    if winner == GAMETREE_PLAYER:
    #        ai_wins += 1
    #elapsed_time = time.time() - start_time

    #average_moves = total_moves / 50

    #print("Average Number of Moves: {:.2f}".format(average_moves))
    #print("GAMETREE_PLAYER Wins: {}/50".format(ai_wins))
    #print("Elapsed Time: {0:.2f} seconds".format(elapsed_time))
    #
    #
        
    """
    You can modify PlayGame function for writing the report
    Modify the FindBestAction in GameTreePlayer class to implement Game tree search.
    You can add functions to GameTreePlayer class as required.
    """

    """
        The above code (PlayGame()) must be COMMENTED while submitting this program.
        The below code (RunTestCase()) must be UNCOMMENTED while submitting this program.
        Output should be your rollnumber and the bestAction.
        See the code for RunTestCase() to understand what is expected.
    """
    
    RunTestCase()


if __name__ == '__main__':
    main()