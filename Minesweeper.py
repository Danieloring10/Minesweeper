import pygame
from pygame.locals import *
import time
from random import randrange

def grid(window, size, rows):
    distanceBtwRows = size // rows
    x = 0
    y = 0
    for i in range(rows):
        x += distanceBtwRows
        y += distanceBtwRows


        pygame.draw.line(window, (0,0,0), (0,x), (size,x))
        
        pygame.draw.line(window, (0,0,0), (y,0), (y,size))

def Text(window, display, pos):
    squareLeng = size // rows 
    font = pygame.font.Font('freesansbold.ttf', 300//rows)
    text = font.render(str(display), True, (0,0,0), None)
    textRect = text.get_rect()
    textRect.center = (pos[0]*squareLeng+squareLeng*.5,pos[1]*squareLeng+squareLeng*.5)
     
    window.blit(text, textRect)

def Open(window):
    squareLeng = size // rows
    MousePos = pygame.mouse.get_pos()
    PosX = MousePos[0]//squareLeng
    PosY = MousePos[1]//squareLeng
    if Area[rows*(PosY)+(PosX)][2] != -1:
        floodFillUtil(window,Area[rows*(PosY)+(PosX)][0],Area[rows*(PosY)+(PosX)][1])
        
    elif Area[rows*(PosY)+(PosX)][2] == -1:
        squareLeng = size // rows
        for j in Mines:            
            pygame.draw.rect(window, (255,0,0), pygame.Rect(j[0]*squareLeng,j[1]*squareLeng,squareLeng,squareLeng))
        play = False
        

def floodFillUtil(window,x,y):
    squareLeng = size // rows
    Coords = (y*rows)+x
    if (x < 0 or x >= rows or y < 0 or y >= rows or
        #Area[Coords][3] != 0 or
        #Area[Coords][3] != 1 or
        Area[Coords][3] == 2):
        return
    
    if (Area[Coords][3] == 1):
        color = (255 - (Area[rows*(y)+(x)][2]*30),255 - (Area[rows*(y)+(x)][2]*30),255 - (Area[rows*(y)+(x)][2]*30))
        pygame.draw.rect(window, color, pygame.Rect(x*squareLeng, y*squareLeng, squareLeng, squareLeng)) 
        pos  = Area[rows*(y)+(x)]   
        Text(window, pos[2], pos)
        Area[(y*rows)+x][3] = 2
        return



    print(Area[(y*rows)+x])
    Area[(y*rows)+x][3] = 2
    color = (247,191,93)
    pygame.draw.rect(window, color, pygame.Rect(x*squareLeng, y*squareLeng, squareLeng, squareLeng))
 
    floodFillUtil(window,x + 1, y)
    floodFillUtil(window,x - 1, y)
    floodFillUtil(window,x, y + 1)
    floodFillUtil(window,x, y - 1)
    
def Check_0(window,Orig):
    print("a")

def Mines_F(window, Mines):
    global Area
    Area = []
    for y in range(rows):
        for x in range(rows):
            Area.append([x,y,0,0,0])
    squareLeng = size // rows    
    for j in Mines:        
        #Area
        PosX = j[0]
        PosY = j[1]
        if PosY != rows:    
            Area[rows*(PosY+1)+(PosX)][2] += 1 # Down 
            Area[rows*(PosY+1)+(PosX)][3] = 1
            if PosX != rows:
                Area[rows*(PosY+1)+(PosX+1)][2] += 1 # Down Rigth
                Area[rows*(PosY+1)+(PosX+1)][3] = 1
            if PosX != 0:    
                Area[rows*(PosY+1)+(PosX-1)][2] += 1 # Down Left
                Area[rows*(PosY+1)+(PosX-1)][3] = 1

        if PosY != 0:   
            Area[rows*(PosY-1)+(PosX)][2] += 1 # Up  
            Area[rows*(PosY-1)+(PosX)][3] = 1
            if PosX != rows:
                Area[rows*(PosY-1)+(PosX+1)][2] += 1 # Up Rigth
                Area[rows*(PosY-1)+(PosX+1)][3] = 1
            if PosX != 0:
                Area[rows*(PosY-1)+(PosX-1)][2] += 1 # Up Left
                Area[rows*(PosY-1)+(PosX-1)][3] = 1

        if PosX != rows:
            Area[rows*(PosY)+(PosX+1)][2] += 1 # Rigth
            Area[rows*(PosY)+(PosX+1)][3] = 1
        if PosX != 0:
            Area[rows*(PosY)+(PosX-1)][2] += 1 # Left 
            Area[rows*(PosY)+(PosX-1)][3]  = 1
    for j in Mines:
        Area[(j[1]*rows)+j[0]][2] = -1
        Area[(j[1]*rows)+j[0]][3] = 3
    

def flag(window, size, rows):        
    squareLeng = size // rows
    MousePos = pygame.mouse.get_pos()
    x = MousePos[0]//squareLeng
    y = MousePos[1]//squareLeng    
    if Area[rows*(y)+(x)][3] == 2:
        return
    if Area[rows*(y)+(x)][4] != 1:
        pygame.draw.rect(window, (255,0,255), pygame.Rect(x*squareLeng,y*squareLeng,squareLeng,squareLeng))
        Area[rows*(y)+(x)][4] = 1
    else:
        pygame.draw.rect(window, (0,150,0), pygame.Rect(x*squareLeng,y*squareLeng,squareLeng,squareLeng))
        Area[rows*(y)+(x)][4] = 0
def redraw(window):
    global size, rows    
    event = pygame.event.wait()
    grid(window, size, rows)
    if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[2] == True:
        flag(window, size, rows)  
    if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] == True:
        Open(window) 
    pygame.display.update()

def main():

    global size, rows, Area, Mines, play
    size = 500
    rows = 20
    Mines = []
    newMine = [randrange(0,rows-1),randrange(0, rows-1)]
    Mines.append(newMine) 
    for i in range(40):
        newMine = [randrange(0,rows-1),randrange(0, rows-1)]        
        for j in Mines: 
            while newMine == j:   
                newMine = [randrange(0,rows-1),randrange(0, rows-1)]         
                for i in Mines:
                    if newMine == i:
                        newMine = [randrange(0,rows-1),randrange(0, rows-1)]         
 
        Mines.append(newMine) 
                
    window = pygame.display.set_mode((size,size))

    
    window.fill((0,150,0))    
    Mines_F(window, Mines)

    play = True

    while play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        redraw(window)
pygame.init()
main()