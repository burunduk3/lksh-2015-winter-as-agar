import json, socket, time
                    
sock = socket.socket()
old_data = ""

def registerMe(name):     
    global sock, tcp_ip, tcp_port

    inf = open('config.txt', 'r')
    config = inf.readline()
    tcp_ip, tcp_port = config.split(' ')
    tcp_port = int(tcp_port)
                                  
    sock.connect((tcp_ip, tcp_port))
    id = json.loads(str(sock.recv(1024), 'utf-8'))['id']
    jdata = dict()
    jdata['name'] = name
    s = json.dumps(jdata) 
    sock.send(bytes(s, 'utf-8'))
    return id
             
def getField():
    global sock, old_data    
    data = sock.recv(1024)
    data = str(data, 'utf-8')

    s = old_data+data
    l = s.split('\n')

    if data[-1] == '\n':
        old_data = ""
        return l[-1]
    else:
        old_data = l[-1]
        if len(l) > 1:
            return l[-2]
        else:
            return [0]         

def sendMe(p):
    global sock
    data = json.dumps(p)
    sock.send(bytes(data, 'utf-8'))

def killMe():
    global sock
    #sock.send(bytes('killme', 'utf-8'))
    sock.close()  
