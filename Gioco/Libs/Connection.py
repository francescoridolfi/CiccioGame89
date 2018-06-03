import time, datetime, socket, ast

class Conn(object):
    isConn = False
    def __init__(self,host,port,buffer=1024):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.buffer = buffer
    def connStarted(self):
        return self.isConn
    def startConn(self):
        if not self.connStarted():
            self.conn.connect((self.host,self.port))
            self.isConn = True
    def getDateTime(self, ms):
        return str(datetime.datetime.fromtimestamp(ms/1000)).split(" ")[1].split(".")[0]
    def getMillisTime(self):
        return round(time.time()*1000)
    def makeUpdate(self, Type, Player, x=None, y=None, Text=None):
        if(Type == "Location"):
            if(x != None and y != None):
                return {"update":{"player":Player,"type":Type,"x":x,"y":y,"time":self.getMillisTime()}}
            else:
                print("Error: no value found for X and Y")
        elif(Type == "Chat"):
            if(Text != None):
                return {"update":{"player":Player,"type":Type,"text":Text,"time":self.getMillisTime()}}
            else:
                print("Error: no value found for Text")
    def getChat(self):
        if(self.isConn):
            req = {"request":"getChat"}
            self.conn.send(str(req).encode())
            data = self.conn.recv(self.buffer).decode()
            if(data == "{}"):
                return {}
            return ast.literal_eval(data)
    def getLocations(self):
        if(self.isConn):
            req = {"request":"getLocations"}
            self.conn.send(str(req).encode())
            data = self.conn.recv(self.buffer).decode()
            if(data == "{}"):
                return {}
            return ast.literal_eval(data)
        else:
            return {"error":"Connection not already started!"}
    def sendUpdate(self,update):
        if(self.isConn):
            self.conn.send(str(update).encode())
            data = self.conn.recv(self.buffer).decode()
            return ast.literal_eval(data)
        else:
            return {"error":"Connection not already started!"}
    
