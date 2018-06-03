import pygame, time, socket, ast
from random import randint
from Libs.Connection import Conn
from Libs.GUI import GUI


pygame.init()

img_path = "Images/"
font_path = "Fonts/"


def getIMG(name):
    img = pygame.image.load(img_path+name)
    return img

def getFont(name,size=10):
    f = pygame.font.Font(font_path+name,size)
    return f



host = input("Inserire l'host del server: ")
port = input("Inserire la porta del server(9999 Default): ")
port = (int(port) if port != "" else 9999)
nick = input("Perfavore scegli un nickname: ")

conn = Conn(host,port)
conn.startConn()

fonts = [getFont("Avenir3.otf",30),getFont("alternate gothic no2.ttf",20)]
avatar = getIMG("player.png")
speed = 5


s_size = (1080,820)
s_bgcolor = (87, 88, 89)

display = pygame.display

screen = display.set_mode(s_size)
display.set_caption("CiccioGame89")
display.flip()

gui = GUI(screen,display,fonts,avatar,nick,conn)

x = 100
y = 100

Process = True
writing = False

text = "Cliccami per scrivere!"

while Process:
    screen.fill(s_bgcolor)
    msg = fonts[1].render(text, True, (255,255,255))
    screen.blit(msg,(695,185))
    elements = gui.runDisplay()
    xy = elements[0]
    box = elements[1]
    x = xy[0]
    y = xy[1]
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            Process = False
            pygame.quit()
            print("Game ended at: "+time.ctime())
            exit()
        if(event.type == pygame.MOUSEBUTTONDOWN):
            if(box.collidepoint(event.pos)):
                text = ""
                writing = True
        if(event.type == pygame.KEYDOWN):
            if writing:
                if(event.key == pygame.K_RETURN):
                    gui.sendMessage(text)
                    text = "Cliccami per scrivere!"
                    writing = False
                elif(event.key == pygame.K_BACKSPACE):
                    text = text[:-1]
                else:
                    text += event.unicode
            else:
                pass
    try:
        if not writing:
            keys = pygame.key.get_pressed()
            if(keys[pygame.K_UP]):
                y=y-speed
            if(keys[pygame.K_DOWN]):
                y=y+speed
            if(keys[pygame.K_RIGHT]):
                x=x+speed
            if(keys[pygame.K_LEFT]):
                x=x-speed
            if(x<0):
                x=0
            if(x>960):
                x=960
            if(y<30):
                y=30
            if(y>720):
                y=720
    except:
        pass
    #print("x: %s, y: %s" % (x,y))
    gui.setPos(x,y)

