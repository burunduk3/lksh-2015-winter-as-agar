import json, socket, time

from constants import *
sock = socket.socket()
old_data = ""
old_json = []

def registerMe(name):     
    global sock, tcp_ip, tcp_port

    inf = open('config.txt', 'r')
    config = inf.readline()
    tcp_ip, tcp_port = config.split(' ')
    tcp_port = int(tcp_port)
                                  
    sock.connect((tcp_ip, tcp_port))
    id = json.loads(str(sock.recv(MAX_LENGTH), 'utf-8'))['id']
    jdata = dict()
    jdata['name'] = name
    s = json.dumps(jdata) 
    sock.send(bytes(s + '\n', 'utf-8'))
    return id

def dearch(data):
    for pl in data:
        buf = []
        for b in pl['balls']:
            buf.append({'x' : b[0], 'y' : b[1], 'm' : b[2]})
        pl['balls'] = buf
    return data
             
def getField():
    global sock, old_data, old_json    
    data = sock.recv(MAX_LENGTH)
    data = str(data, 'utf-8')

    s = old_data+data            
    l = s.split('\n')

    old_data = l[-1]
    if len(l) > 1:
        old_json = dearch(json.loads(l[-2]))
    if DEBUG_PROTOCOL_PRINT:
        print(old_json)
    return old_json

def sendMe(p):
    global sock
    data = json.dumps(p)
    sock.send(bytes(data + '\n', 'utf-8'))

def killMe():
    global sock
    #sock.send(bytes('killme', 'utf-8'))
    sock.close()  
