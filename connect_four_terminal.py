

import numpy as np
#import pygame
import sys

class Board:
  def __init__(self):
    self.gameover = False
    self.array = np.zeros((6,7))
    self.turn = 0

  def gameover_check(self):
    for position in self.array[0]:
      if position>0:
        self.gameover = True

    return self.gameover

  def new_turn(self):
    if self.p1move() is True:
      if self.p2move() is True:
        self.turn+=1

  def columnFull(self):
      return False

  def win_condition(self):
    COLS = 7
    ROWS = 6
    count = 1
    for ROW in range(ROWS-3):
      for COL in range(COLS):
        if self.array[ROW][COL]==self.array[ROW+1][COL]==self.array[ROW+2][COL]==self.array[ROW+3][COL] and self.array[ROW][COL]!=0:
          return self.array[ROW][COL]
    for ROW in range(ROWS):
      for COL in range(COLS-3):
        if self.array[ROW][COL]==self.array[ROW][COL+1]==self.array[ROW][COL+2]==self.array[ROW][COL+3] and self.array[ROW][COL]!=0:
          return self.array[ROW][COL]
    for ROW in range(ROWS-3):
      for COL in range(COLS-3):
        if self.array[ROW][COL]==self.array[ROW+1][COL+1]==self.array[ROW+2][COL+2]==self.array[ROW+3][COL+3] and self.array[ROW][COL]!=0:
          return self.array[ROW][COL]
    for ROW in range(3,ROWS):
      for COL in range(COLS-3):
        if self.array[ROW][COL]==self.array[ROW-1][COL+1]==self.array[ROW-2][COL+2]==self.array[ROW-3][COL+3] and self.array[ROW][COL]!=0:
          return self.array[ROW][COL]
    return 0

  def print_board(self):
    print(self.array)

  def move(self, column, player):
      print("newboard\n")
      if self.columnFull():
          print("here")
          return False
      row = 0
      x = 0
      while row <= 5:
          x = self.array [row][column]
          print("row =", row)
          print("x = ", x)
          #print (str(x))
          if x != 0:
            print("Found a piece in row ", row)
            break
          row += 1
          #if x!=0:
            #print("hello\n")
            #self.array[row-1][column]=player
      
      if row - 1 >= 0:
        print("Inserting piece in row ", row-1)
        self.array [row-1][column] = player  
      else:
        print(f"Column {column} is full! Can't insert piece here")
      self.print_board()

def main():
  board1=Board()
  board1.print_board()
  player1=True
  Player2=False
  gameover=False
  numberofmoves=0
  while gameover==False:
    if player1==True:
      print("place a piece")
      column=int(input("select column"))
      if int (column)>6 or int (column)<0:
        print("pick a correct column")
      board1.move(column,1)
      player1=False
      player2=True
    if(numberofmoves>4):
      winner=board1.win_condition()
      print (str(winner))
      if winner==1:
        gameover=True
        print("player one wins")
      elif winner==2:
        gameover=True
        print("player two wins")
      elif winner==0:
        continue
    numberofmoves=numberofmoves+1
    if player2==True:
      print("place a piece")
      column=int(input("select column"))
      if int(column)>6 or int(column)<0:
        print("pick a correct column")
      board1.move(column,2)
      player1=True
      player2=False
    numberofmoves=numberofmoves+1
    print("number of moves = " + (str(numberofmoves)))
    if(numberofmoves>4):
      winner=board1.win_condition()
      print (str(winner))
      if winner==1:
        gameover=True
        print("player one wins")
      elif winner==2:
        gameover=True
        print("player two wins")
      elif winner==0:
        continue
    

main()
