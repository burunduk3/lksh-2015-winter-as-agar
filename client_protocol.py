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
    l = s.strip().split('\n')

    if len(l) > 0:
        if data[-1] == '\n':
            old_data = ""
            print("1 = ", l[-1])
            return json.loads(l[-1])
        else:
            old_data = l[-1]
            if len(l) > 1:
                print("2 = ", l[-2])
                return json.loads(l[-2])
            else:
                print("3 = ", [])
                return ([]) 
    else:
        print("4 = ", []) 
        return([])       

def sendMe(p):
    global sock
    data = json.dumps(p)
    sock.send(bytes(data, 'utf-8'))

def killMe():
    global sock
    #sock.send(bytes('killme', 'utf-8'))
    sock.close()  