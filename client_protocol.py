import json, socket, time

from constants import *
from bz2 import compress, decompress
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
    data = sock.recv(MAX_LENGTH)
    # id = json.loads(str(decompress(data), 'utf-8'))['id']
    id = json.loads(str(data, 'utf-8'))['id']
    jdata = dict()
    jdata['name'] = name
    s = json.dumps(jdata) 
    # sock.send(compress(bytes(s + '\n', 'utf-8')))
    sock.send(bytes(s + '\n', 'utf-8'))
    return id
             
def getField():
    global sock, old_data, old_json    
    # data = decompress(sock.recv(MAX_LENGTH))
    data = sock.recv(MAX_LENGTH)
    data = str(data, 'utf-8')
    s = old_data+data            
    l = s.split('\n')

    old_data = l[-1]
    if len(l) > 1:
        old_json = json.loads(l[-2])
    if DEBUG_PROTOCOL_PRINT:
        print(old_json)
    return old_json

def sendMe(p):
    global sock
    data = json.dumps(p)
    # sock.send(compress(bytes(data + '\n', 'utf-8')))
    sock.send(bytes(data + '\n', 'utf-8'))

def killMe():
    global sock
    #sock.send(bytes('killme', 'utf-8'))
    sock.close()  
