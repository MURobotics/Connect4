import numpy as np
import pygame
import sys
import random
import math

BLUE=(0,0,255)
BLACK=(0,0,0)
RED=(255,0,0)
YELLOW=(255,255,0)
COLS=7
ROWS=6

#initialize pygame and variables for the screen.
pygame.init()
SQUARESIZE=100
width=COLS*SQUARESIZE
height=(ROWS+1)*SQUARESIZE
size=(width,height)
RADIUS = int(SQUARESIZE/2-5)
screen=pygame.display.set_mode(size)



class Board:
  def __init__(self,array=np.zeros((6,7))):
    self.gameover = False
    self.array = array
    self.turn = 0



#create a copy of the board for the minimax function to test different moves.\
  def copyBoard(self):
    return self.array.copy()

  def columnFull(self):
      return False
# iterate over entire board to search for four connected pieces which would indicate one of the players winning.
  def win_condition(self):
    COLS = 7
    ROWS = 6

    for COL in range(COLS-3):
      for ROW in range(ROWS):
        if (self.array[ROW][COL]==self.array[ROW][COL+1]==self.array[ROW][COL+2]==self.array[ROW][COL+3]) and self.array[ROW][COL]!=0:
          return self.array[ROW][COL]

    for COL in range(COLS):
      for ROW in range(ROWS-3):
        if (self.array[ROW][COL]==self.array[ROW+1][COL]==self.array[ROW+2][COL]==self.array[ROW+3][COL]) and self.array[ROW][COL]!=0:
          return self.array[ROW][COL]

    for COL in range(COLS-3):
      for ROW in range(ROWS-3):
        if (self.array[ROW][COL]==self.array[ROW+1][COL+1]==self.array[ROW+2][COL+2]==self.array[ROW+3][COL+3]) and self.array[ROW][COL]!=0:
          return self.array[ROW][COL]

    for COL in range(COLS-3):
      for ROW in range(3,ROWS):
        if (self.array[ROW][COL]==self.array[ROW-1][COL+1]==self.array[ROW-2][COL+2]==self.array[ROW-3][COL+3]) and self.array[ROW][COL]!=0:
          return self.array[ROW][COL]

    return 0

# prints out the current state of the board.
  def print_board(self):
    print("\n [0  1  2  3  4  5  6]")
    print(self.array)


#draws the current board on the screen.  
  def draw_board(self):
    COLS=7
    ROWS=6
    self.array=np.flipud(self.array)
    for col in range(COLS):
      for row in range(ROWS):
        pygame.draw.rect(screen, BLUE, (col*SQUARESIZE,row*SQUARESIZE+SQUARESIZE,SQUARESIZE,SQUARESIZE))
        pygame.draw.circle(screen,BLACK,(int(col*SQUARESIZE+SQUARESIZE/2),int(row*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)),RADIUS)

    for col in range(COLS):
      for row in range(ROWS):
        if self.array[row][col]==1:
          pygame.draw.circle(screen,RED,(int(col*SQUARESIZE+SQUARESIZE/2),height-int(row*SQUARESIZE+SQUARESIZE/2)),RADIUS)
        elif self.array[row][col]==2:
          pygame.draw.circle(screen,YELLOW,((int(col*SQUARESIZE+SQUARESIZE/2)),height-(int(row*SQUARESIZE+SQUARESIZE/2))),RADIUS)
    pygame.display.update()
    self.array=np.flipud(self.array)

  def isvalidlocation(self, col:int):
    if self.array[0][col]==0:
      return True
    return False

#Iterates over the board and assigns a score based on how many pieces have been connected by a player.
  def window_score(self,window, player): 
    score=0
    if window.count(player)==4:
      score+=100
    elif window.count(player)==3 and window.count(0)==1:
      score+=80
    elif window.count(player)==2 and window.count(0)==2:
      score+=50
    elif window.count(player)==1 and window.count(0)==3:
      score+=25
    elif window.count(1)==3 and window.count(0)==1:
      score-=1000
    elif window.count(1)==2 and window.count(0)==2:
      score-=300
    elif window.count(1)==4:
      score-=100000000

    return score

#Assigns a score to a possible move and return that score.
  def heuristic(self, player):
    score=0

    #check the number of connected pieces horizontally
    for r in range(0,6):
      row = [int(i) for i in list(self.array[r,:])]
      for c in range(0,4):
        window=row[c:c+4]
        score+=self.window_score(window, player)

    #check the number of connected pieces vertically
    for c in range(0,7):
      col = [int(i) for i in list(self.array[:,c])]
      for r in range(0,3):
        window=col[r:r+4]
        score+=self.window_score(window, player)

    #check the number of connected pieces on positive diagonal
    for c in range(0,4):
      for r in range(0,3):
        window=[self.array[r+i][c+i] for i in range(0,4)]
        score+=self.window_score(window, player)
    
    #check the number of connected pieces on negative diagonal
    for c in range(3,7):
      for r in range(0,3):
        window=[self.array[r+i][c-i] for i in range(0,4)]
        score+=self.window_score(window, player)
    return score



#places a players piece in the specified column.
  def move(self, col, player):
      row = 0
      if self.isvalidlocation(col):
        x = 0
        while row <= 5:
          x = self.array [row][col]
          if x != 0:
            break
          row += 1
      
      
      if row >= 0 and row<7:
        self.array[row-1][col] = player  
      else:
        #print(f"Column {col} is full! Can't insert piece here")
        col=int(input("select a valid column"))
        self.move(col,player)

#searches the top row of the board for columns that haven't been filled.
  def valid_moves(self):
    top_row=[]
    for col in range(0,7):
      if self.isvalidlocation(col):
        top_row.append(col)
    return top_row

#function that return the terminal state of the game
  def terminal_state(self):
    if self.win_condition()!=0 or len(self.valid_moves())==0:
      return True
    return False


def minimax(board1,depth,alpha,beta,maximizer):
  validmoves=board1.valid_moves()
  if board1.terminal_state():
    if board1.win_condition()==1:
      return -1000000,None
    
    if board1.win_condition()==2:
      return 1000000,None
    return 0,None

  if depth==0:
    return board1.heuristic(2),None
  
  if (maximizer==True):
    value= -math.inf
    choice=random.choice(validmoves)

    for move in validmoves:
      child=Board(board1.copyBoard())
      child.move(move,2)

      temp=(minimax(child,depth-1,alpha,beta,False)[0])
      
      if temp>value:
        value=temp
        choice=move
      alpha=max(alpha,value)
      if alpha>=beta:
        break

    return value,choice

  else:
    value=math.inf
    choice=random.choice(validmoves)
    for move in validmoves:
      child=Board (board1.copyBoard())
      child.move(move,1)
      
      temp=(minimax(child,depth-1,alpha,beta,True)[0])

      if temp<value:
        value=temp
        choice=move
      beta=min(beta,value)

      if beta<=alpha:
        break

    return value,choice
    

player1=True
player2=False

def main():
  board1=Board()
  board1.__init__()
  board1.draw_board()
  pygame.display.update()
  board1.print_board()
  global player1
  global player2
  gameover=False
  numberofmoves=0
  while gameover==False:
    for event in pygame.event.get():
      if event.type==pygame.QUIT:
        sys.exit()
      if event.type==pygame.MOUSEMOTION:
        pygame.draw.rect(screen,BLACK,(0,0,width,SQUARESIZE))
        posx=event.pos[0]
        pygame.draw.circle(screen, RED,(posx,int(SQUARESIZE/2)), RADIUS)
      pygame.display.update()
      if event.type==pygame.MOUSEBUTTONDOWN:
        pygame.draw.rect(screen,BLACK,(0,0,width,SQUARESIZE))
        if player1==True:
          posx=event.pos[0]
          col=int(math.floor(posx/SQUARESIZE))
          if board1.isvalidlocation(col):
            board1.move(col,1)
            player1=False
            player2=True
            board1.draw_board()
            numberofmoves=numberofmoves+1
            if(numberofmoves>=4):
              winner=board1.win_condition()
              if winner==1:
                gameover=True
                print("player one wins")
                pygame.time.wait(3000)
                sys.exit()
              elif winner==2:
                gameover=True
                print("player two wins")
                pygame.time.wait(3000)
                sys.exit()
        if player2==True:
          temp=Board(board1.copyBoard())
          selection=minimax(temp,5,-math.inf,math.inf,True)[1]
          board1.move(selection,2)
          board1.print_board()
          player2=False
          player1=True
          board1.draw_board()
          if(numberofmoves>=4):
            winner=board1.win_condition()
            if winner==1:
              gameover=True
              print("player one wins")
              pygame.time.wait(3000)
              sys.exit()
            elif winner==2:
              gameover=True
              print("player two wins")
              pygame.time.wait(3000)
              sys.exit()
        

main()