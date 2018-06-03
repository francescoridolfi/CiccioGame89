import pygame, time, ast, datetime

class GUI(object):
    def __init__(self,screen,display,fonts,avatar,nickname,conn):
        self.screen = screen
        self.display = display
        self.fonts = fonts
        self.avatar = avatar
        self.nickname = nickname
        self.conn = conn
        self.x = 100
        self.y = 100
    def getChat(self):
        chat = self.conn.getChat()
        screen = self.screen
        i=35
        rect = pygame.Rect(690,30,360,i*5-25)
        pygame.draw.rect(screen,(0,0,0),rect,2)
        for msg in chat:
            text = self.fonts[1].render("["+self.conn.getDateTime(msg)+"] "+chat[msg]["from"]+" > "+chat[msg]["text"],True,(255,255,255))
            screen.blit(text,(700,i))
            i += 30
        box = pygame.Rect(690,180,360,30)
        pygame.draw.rect(screen,(0,0,0),box,2)
        return box
    def getLocs(self):
        locs = self.conn.getLocations()
        screen = self.screen
        for player in locs:
            x = locs[player]["x"]
            y = locs[player]["y"]
            if(player == self.nickname):
                self.x = x
                self.y = y
            nick = self.fonts[0].render(player,True,(255,255,255))
            screen.blit(nick,(x,y-30))
            screen.blit(pygame.transform.scale(self.avatar,(100,100)),(x,y))
        if(self.nickname not in locs):
            nick = self.fonts[0].render(self.nickname,True,(255,255,255))
            screen.blit(nick,(self.x,self.y-30))
            screen.blit(pygame.transform.scale(self.avatar,(100,100)),(self.x,self.y))
            return [self.x,self.y]
        if(self.nickname in locs):
            x = locs[self.nickname]["x"]
            y = locs[self.nickname]["y"]
            return [x,y]
    def runDisplay(self):
        xy = self.getLocs()
        box = self.getChat()
        self.display.update()
        elements = [xy,box]
        return elements
    def sendMessage(self,msg):
        up = self.conn.makeUpdate("Chat",self.nickname,Text=msg)
        resp = self.conn.sendUpdate(up)
        if("error" in resp):
            print(resp["error"])
    def setPos(self,x,y):
        up = self.conn.makeUpdate("Location",self.nickname,x,y)
        resp = self.conn.sendUpdate(up)
        if("error" in resp):
            print(resp["error"])

