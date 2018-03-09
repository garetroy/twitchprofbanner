import json
import re
import socket

def loadJson():
    with open("data.json") as json_data:
        jdata = json.load(json_data)

    return jdata

def get_sender(msg):
    result = ""
    for char in msg:
        if char == "!":
            break
        if char != ":":
            result += char
    return result

def get_message(msg):
    result = ""
    i = 3
    length = len(msg)
    while i < length:
        result += msg[i] + " "
        i += 1
    result = result.lstrip(':')
    return result


def parse_message(msg):
    if len(msg) >= 1:
        msg = msg.split(' ')

class Bot:
    def __init__(self,channel,oath):
        self.host     = "irc.twitch.tv"
        self.port     = 6667
        self.nick     = "destroyerofbad"
        self.channel  = channel
        self.oath     = oath
        self.client   = None

    def sendMessage(self,string):
        if(self.client == None):
            print("Cannot send message, client not connected")
            return 

        self.client.send(bytes(string+"\r\n",'UTF-8'))

    def connect(self):
        self.client = socket.socket()
        self.client.connect((self.host,self.port))

    def joinChannel(self):
        self.sendMessage("PASS {}".format(self.oath))
        self.sendMessage("NICK {}".format(self.nick))
        self.sendMessage("JOIN {}".format(self.channel))

    def monitor(self):
        data = ""
        while True:
            data = data+self.client.recv(1024).decode('UTF-8')
            data_split = re.split(r"[~\r\n]+", data)
            data = data_split.pop()
    
            for line in data_split:
                line = str.rstrip(line)
                line = str.split(line)
    
                if len(line) >= 1:
                    if line[0] == 'PING':
                        send_pong(line[1])
    
                    if line[1] == 'PRIVMSG':
                        sender = get_sender(line[0])
                        message = get_message(line)
                        parse_message(message)
    
                        print(sender + ": " + message)

data = loadJson()
bot  = Bot(data['chan'],data['oauth'])
bot.connect()
bot.joinChannel()
bot.monitor()
