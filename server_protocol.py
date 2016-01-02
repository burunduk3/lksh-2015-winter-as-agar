import selectors, socket, threading, sys, json, random

poll = selectors.DefaultSelector ()
clients = dict()

a = False
sock = socket.socket()

def initserver():
    global a, sock, poll
    sock = socket.socket()
    sock.bind (('0.0.0.0', 3030))
    sock.listen (10)
    sock.setblocking (False)
    poll.register (sock, selectors.EVENT_READ, accept)

    a = False

    def thr():            
        global a
        while not a:
            events = poll.select()                                       
            for key, mask in events:
                callback = key.data
                callback (key.fileobj, mask)


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
            except BlockingIOError:
                poll.unregister (conn)
                del clients[conn]
                conn.close()
                break
            if not data:
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
                        updatecursor((v["x"], v["y"])                                                                           
                    elif ("name" in v):
                        addPlayer(v["name"], clients[conn])
                    else:
                        print("User specified no name and it isn't cursor")
                except:
                    print("user with id " + str(clients[conn]) + " tried something incorrect")
        mask &=~ selectors.EVENT_READ
    assert mask == 0

def sendMap(id, data):
    for x in clients:
        if (clients[x] == id):
            x.send(bytes(data, 'utf-8'))                                            
 

