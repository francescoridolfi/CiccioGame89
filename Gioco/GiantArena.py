import pygame, time, socket, ast
from random import randint

pygame.init()


frasi = ["Dio Sasso","Dio Mattone","Ti denuncio","Osanna eh"]

img_path = "Images/"
font_path = "Fonts/"

def getIMG(name):
    img = pygame.image.load(img_path+name)
    return img

def getFont(name,size=10):
    f = pygame.font.Font(font_path+name,size)
    return f

def getMillis():
    return round(time.time()*1000)

font = getFont("Avenir3.otf",30)

host = input("Inserire l'host del server: ")
port = input("Inserire la porta del server(9999 Default): ")
port = (int(port) if port != "" else 9999)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))


nick = input("Perfavore scegli un nickname: ")

ciccio = getIMG("player.png")
x=100
y=100
speed = 2

xt = x
yt = y

s_size = (600,400)
s_bgcolor = (87, 88, 89)

display = pygame.display

screen = display.set_mode(s_size)
display.set_caption("GiantArena")
display.flip()

clicks = 0
start = 0

Process = True
pp = False

while Process:
    txt = ""
    xt = x
    yt = y
    screen.fill(s_bgcolor)
    nickname = font.render(nick[:9], True, (255,255,255))
    screen.blit(nickname,(x,y-30))
    screen.blit(pygame.transform.scale(ciccio, (100,100)),(x,y))
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            Process = False
            pygame.quit()
            exit()
        if(event.type == pygame.KEYDOWN):
            if(event.key == 107):
                txt = frasi[randint(0,len(frasi)-1)]
                text = font.render(txt, True, (0,255,0))
                if(y>=280):
                    yt = y - 40
                """if(y<=30):
                    yt = y + 100"""
                if(x>=500):
                    xt = x - 30
                screen.blit(text,(xt,yt))
                pp = True
    try:
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
        if(x>500):
            x=500
        if(y<30):
            y=30
        if(y>306):
            y=306
    except:
        print("Chiusura")
    #print("x: %s, y: %s" % (x,y))
    info = {"player":nick,"properties":{"x":x,"y":y,"frase":("None" if pp == False else txt)}}
    s.send(str(info).encode())
    data = ast.literal_eval(s.recv(1024).decode())
    for k in data:
        if(k != nick):
            x_p = data[k]["x"]
            y_p = data[k]["y"]
            xt_p = x_p
            yt_p = y_p
            n = font.render(k, True, (255,255,255))
            screen.blit(n,(x_p,y_p-30))
            screen.blit(pygame.transform.scale(ciccio, (100,100)), (x_p,y_p))
            if(data[k]["frase"] != "None"):
                text = font.render(data[k]["frase"], True, (0,255,0))
                if(y>=280):
                    yt_p = y_p - 40
                """if(y<=30):
                    yt = y + 100"""
                if(x>=500):
                    xt_p = x_p - 30
                screen.blit(text,(xt_p,yt_p))
                display.update()
                time.sleep(0.1)
    display.update()
    if(pp == True):
        time.sleep(0.1)
        pp = False
print("Game ended at: "+time.ctime())
