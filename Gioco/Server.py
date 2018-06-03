import socket, time, ast, threading
from random import randint


class ThreadedServer(object):
    locations = {}
    chat = {}
    
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def getMillis(self):
        return round(time.time()*1000)

    def listen(self):
        chat = self.chat
        if not chat:
            msg = self.getMillis()
            chat[msg] = {}
            chat[msg]["from"] = "Server"
            chat[msg]["text"] = "server started!"
        print("Listening...")
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            threading.Thread(target = self.listenToClient,args = (client,address)).start()
            print(address[0]+":"+str(address[1])+" connected!")

    def listenToClient(self, client, address):
        size = 1024
        while True:
            try:
                data = client.recv(size)
                if data:
                    info = ast.literal_eval(data.decode())
                    for k in info:
                        if k == "request":
                            if(info["request"] == "getLocations"):
                                data = str(self.locations)
                                if not self.locations:
                                    data = "{}"
                                client.send(data.encode())
                            elif(info["request"] == "getChat"):
                                chat = self.chat
                                msgs = []
                                for k in chat:
                                    msgs.append(k)
                                resp = {}
                                if len(msgs) > 5:
                                    for i in range(len(msgs)-5,len(msgs)):
                                        resp[msgs[i]] = chat[msgs[i]]
                                else:
                                    resp = chat
                                data = str(resp)
                                if not self.chat:
                                    data = "{}"
                                client.send(data.encode())
                        elif k == "update":
                            if(info["update"]["type"] == "Location"):
                                player = info["update"]["player"]
                                self.locations[player] = {}
                                self.locations[player]["x"] = info["update"]["x"]
                                self.locations[player]["y"] = info["update"]["y"]
                                data = {"success":"Location saved!"}
                                client.send(str(data).encode())
                            if(info["update"]["type"] == "Chat"):
                                player = info["update"]["player"]
                                msg = info["update"]["text"]
                                ms = info["update"]["time"]
                                self.chat[ms] = {}
                                self.chat[ms]["from"] = player
                                self.chat[ms]["text"] = msg
                                data = {"success":"Message saved!"}
                                client.send(str(data).encode())
                    #print(self.locations)
                else:
                    raise error('Client disconnected')
            except:
                client.close()
                return False

if __name__ == "__main__":
    while True:
        port_num = input("Port (Default: 9999)? ")
        try:
            port_num = (int(port_num) if port_num != "" else 9999)
            break
        except ValueError:
            pass

    ThreadedServer('',port_num).listen()
