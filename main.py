import pygame
import asyncio
import copy
import time
from sys import exit
class Main():
    def __init__(self) -> None:
        pygame.init()
        self.width=self.height=600
        self.screen=pygame.display.set_mode((self.height,self.width))
        pygame.display.set_caption("TIC TAC TOE" )
        self.X=pygame.image.load("assets/x.png").convert_alpha()
        self.O=pygame.image.load("assets/O.png").convert_alpha()
        self.turn=True
        self.game_ended=False
        self.board_drawn=False
        self.backboard=[['','',''],['','',''],['','','']]
        self.v1=pygame.Rect(200,50,15,500)
        self.v2=pygame.Rect(385,50,15,500)
        self.h1=pygame.Rect(50,200,500,15)
        self.h2=pygame.Rect(50,385,500,15)        
    def draw_board(self):
            pygame.draw.rect(self.screen,'blue',self.v1,border_radius=50)
            pygame.draw.rect(self.screen,'blue',self.v2,border_radius=50)
            pygame.draw.rect(self.screen,'blue',self.h1,border_radius=50)
            pygame.draw.rect(self.screen,'blue',self.h2,border_radius=50)
    def moves_left(self,board):
        empty=[]
        for i in range(3):
            for j in range(3):
                if board[i][j]=='':
                    empty.append([i,j])
        return empty
                    
    def minimax(self,board,ismax):
        winner=self.psuedo_winner(board)
        # print(winner)
        if winner==1:
            return 1,None
        if winner==-1:
            return -1,None
        elif winner==0:
            return 0,None

        if ismax:
            bestscore=-100
            bestmove=None
            for [x,y] in self.moves_left(board):
                tempboard=copy.deepcopy(board)
                tempboard[x][y]=1
                score=self.minimax(tempboard,False)[0]
                if score>bestscore:
                    bestmove=(x,y)
                    bestscore=score
            return (bestscore,bestmove)
        elif not ismax:
            bestmove=None
            bestscore=100
            for [x,y] in self.moves_left(board):
                tempboard=copy.deepcopy(board)
                tempboard[x][y]=-1
                score=self.minimax(tempboard,True)[0]
                if score<bestscore:
                    bestmove=(x,y)
                    bestscore=score
            return (bestscore,bestmove)




    def draw_line(self,start,end,widht=26):
        pygame.draw.line(self.screen,"grey",start,end,width=widht)
        pygame.draw.circle(self.screen, "grey", start, widht/2,)
        pygame.draw.circle(self.screen, "grey", end, widht/2)
    def reset_board(self):
        self.backboard=[['','',''],['','',''],['','','']]
        self.screen.fill("black")
        self.draw_board()
        self.turn=True
        self.board_drawn=False
        self.game_ended=False
        self.update()
    def psuedo_winner(self,board):
        for i in range(3):
            if board[i][0]==board[i][1]==board[i][2]!='':
                return board[i][0] 
        for j in range(3):
            if board[0][j]==board[1][j]==board[2][j]!='':
                return board[0][j]
  
        if board[0][0]==board[1][1]==board[2][2]!='':
            return board[0][0]

        if board[0][2]==board[1][1]==board[2][0]!='':
            return board[2][0]
 
        if self.moves_left(board)==[]:
            return 0

    def check_winner(self):
        for i in range(3):
            if self.backboard[i][0]==self.backboard[i][1]==self.backboard[i][2]!='':
                self.draw_line(self.coordlist[i][0],self.coordlist[i][2])
                self.game_ended=True
        for j in range(3):
            if self.backboard[0][j]==self.backboard[1][j]==self.backboard[2][j]!='':
                self.draw_line(self.coordlist[0][j],self.coordlist[2][j])
                self.game_ended=True
        if self.backboard[0][0]==self.backboard[1][1]==self.backboard[2][2]!='':
            self.draw_line(self.coordlist[0][0],self.coordlist[2][2])
            self.game_ended=True
        if self.backboard[0][2]==self.backboard[1][1]==self.backboard[2][0]!='':
            self.draw_line(self.coordlist[0][2],self.coordlist[2][0])           
            self.game_ended=True
        if self.moves_left(self.backboard)==[]:
            self.game_ended=True
        

    def play_turn(self):
        self.coordlist=[[(125,125),(300,125),(475,125)],[(125,300),(300,300),(475,300)],[(125,475),(300,475),(475,475)]]
        row=col=10
        x,y=pygame.mouse.get_pos()
        if x<self.v1.centerx:col=0
        elif x>self.v1.centerx and x<self.v2.centerx:col=1
        elif x>self.v2.centerx: col=2
        if y<self.h1.centery:row=0
        elif y>self.h1.centery and y<self.h2.centery:row=1
        elif y>self.h2.centerx: row=2

        if self.turn and self.backboard[row][col]=='':
            self.screen.blit(self.X,self.X.get_rect(center=self.coordlist[row][col]))
            self.backboard[row][col]=1
            self.turn=False
            
                        
        # else:
        #     # self.screen.blit(self.O,self.O.get_rect(center=self.coordlist[row][col]))
        #     self.Comp_play()
        #     # self.backboard[row][col]=-1
        #     self.turn=True
        self.check_winner()
        self.update()
    def Comp_play(self):
            move=self.minimax(self.backboard,False)[1]
            if move != None:
                self.screen.blit(self.O,self.O.get_rect(center=self.coordlist[move[0]][move[1]]))
                self.backboard[move[0]][move[1]]=-1
            self.check_winner()
            


    def update(self):
        pygame.display.update()
    async def main(self):
        while True:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type==pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_r] and self.game_ended:
                    print("r pressed")
                    self.reset_board()
                if event.type==pygame.MOUSEBUTTONDOWN and not self.game_ended :
                    self.play_turn()
            if not self.turn :
                self.Comp_play()
                self.turn=True

            if not self.board_drawn:
                self.draw_board()
                self.board_drawn=True

            self.update()
            await asyncio.sleep(0)
            


if __name__=="__main__":
    game=Main()
    asyncio.run(game.main())
  
