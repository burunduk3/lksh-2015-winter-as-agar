import selectors, socket, threading, sys, json, random

poll = selectors.DefaultSelector ()
clients = dict()
localServer = ""

a = False

sock = socket.socket()
def initserver(ss):
    global a, sock, poll, localServer
    localServer = ss
    sock = socket.socket()
    sock.bind (('0.0.0.0', 3030))
    sock.listen (10)
    sock.setblocking (False)
    poll.register (sock, selectors.EVENT_READ, accept)

    a = False

    def thr():            
        global a
        while not a:
            try:
                events = poll.select()                                       
                for key, mask in events:
                    callback = key.data
                    callback (key.fileobj, mask)
            except:
                print("One of users died")


    threading.Thread(target = thr, daemon=True).start() 
                                        
    while not a:
        v = sys.stdin.readline().strip()
        #print(v)
        if (v == "quit"):   
            a = True
        
cnt = random.randint(1, 10**40)
v = dict()
def accept (server, mask):
    global poll, cnt
    if mask & selectors.EVENT_READ:
        while True:
            try:
                conn, addr = sock.accept ()     
                print("Connected: " + str(addr))
                v["id"] = cnt                                  
                conn.send(bytes(json.dumps(v), 'utf-8'))
            except BlockingIOError:
                break
            conn.setblocking (False)
            poll.register (conn, selectors.EVENT_READ, read)
            clients[conn] = cnt
            cnt = random.randint(1, 10**40) 
        mask &=~ selectors.EVENT_READ
    assert mask == 0

def read (conn, mask):
    if mask & selectors.EVENT_READ:
        while True:
            try:
                data = conn.recv(1024)
                print(data)   
            except BlockingIOError:
                break
            if not data:
                print("deleting user " + str(clients[conn]))
                poll.unregister (conn)
                del clients[conn]
                conn.close()
                break
            else:
                data = data.decode()            
                print(data)
                try:               
                    v = json.loads(data)                                                     
                    v["id"] = clients[conn]
                    if ("x" in v):      
                        localServer.updatecursor(v)
                    elif ("name" in v):                     
                        localServer.addPlayer(v["name"], clients[conn])
                    else:
                        print("User specified no name and it isn't cursor")
                except TypeError:
                    print("user with id " + str(clients[conn]) + " tried something incorrect")
                except :
                    print("Server failed in to add player or update cursor")
        mask &=~ selectors.EVENT_READ
    assert mask == 0

def sendMap(id, data):
    global localServer
        data = json.dumps(data)       
        for x in clients:
            try:
                if (clients[x] == id):
                    x.send(bytes(data, 'utf-8'))
            except:
                print("deleting user " + str(clients[x]))
                poll.unregister(x)                
                x.close()                                
                del clients[x]
                localServer.UserExit(id)       
