import json, socket

tcp_ip = '192.168.3.49'
tcp_port = 3030

sock = socket.socket()

def registerMe(name):     
    global sock, tcp_ip, tcp_port        
    sock.connect((tcp_ip, tcp_port))
    id = json.loads(str(sock.recv(1024), 'utf-8'))['id']
    jdata = dict()
    jdata['name'] = name
    s = json.dumps(jdata) 
    sock.send(bytes(s, 'utf-8'))
    return id

def getField():
    global sock    
    data = sock.recv(1024)
    data = str(data, 'utf-8')
    return json.loads(data)

def sendMe(p):
    global sock
    data = json.damps(p)   
    sock.send(bytes(data, 'utf-8'))

def killMe():
    global sock
    #sock.send(bytes('killme', 'utf-8'))
    sock.close()