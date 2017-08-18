import asyncore 
import logging
import socket
import redis
import time
#import handler as EchoHandler

# Define
r_server = redis.Redis("localhost")
logging.basicConfig()
logger = logging.getLogger()

# het ziet er naar uit dat de msgbus alles moet verwerken.
# wat dus niet de bedoeling is!!

"""
Voor JSON support:
import redis
conn = redis.Redis('localhost')

user = {"Name":"Pradeep", "Company":"SCTL", "Address":"Mumbai", "Location":"RCP"}

conn.hmset("pythonDict", user)

conn.hgetall("pythonDict")
Wel json load / dump nodig
"""


# echo moet ook een naming mogelijkheid krijgen, inplaats van PORT.
# IF INT of ELSE, naming komt dan weer uit REDIS

# Redis Name coversie werkt nogsteeds niet goed...

# deze later nog uitbreiden met CV stream send mogelijkheid.
# ook mini berichten via sysv_ipc (wel nakijken of dit echt voordeel heeft, bericht kunnen maar mini zijn)
#

def Echo(port, message):
    logger.debug("Call on Port: %s" % port)
    logger.debug("With message: %s" % message)
    if(isinstance(port, int)):
        ip = socket.gethostname() # dit zou ook dynamic moeten
        #time.sleep(5)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))  # IP must be dynamic
        s.sendall(message)
        data = s.recv(1024) # not to big.
        s.close()
        return (data)
    elif(r_server.get(port) is None):
        logger.warning("ERROR! no Name or Port given!!! Get out!!!")
        logger.warning("ERROR port: %s" % port)
        logger.debug("Possible: %s" % r_server.lrange("bus", 0, -1))
        logger.warning("ERROR message: %s" % message)
        #print r_server.get(port)
        #print "ERROR! no/wrong Name or Port given!!!"
    elif(isinstance(port, str)):
        ns = int(r_server.get(port))
        ip = socket.gethostname()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, ns))
        s.sendall(message)
        data = s.recv(1024)
        s.close()
        return (data)

class EchoHandler(asyncore.dispatcher):
    # er zijn hier wel errors:
    # EchoServer instance has no attribute '__trunc__' -> handle_read|57
    # EchoHandler instance has no attribute 'data' -> handle_write|50
    def __init__(self, queue, name, sock, chunk_size=256):
        self._logger = logging.getLogger(__name__)
        self.queue = queue
        self.chunk_size = chunk_size
        # hier onder de naam van de aanvrager in debug info.
        # + sock = IP alleen...
        self.logger = logging.getLogger('EchoHandler %s' % str(sock.getsockname()))
        self.out_buffer = ''
        asyncore.dispatcher.__init__(self, sock=sock)
        self.data_to_write = []
        self.name = name
        return
    
    def writable(self):
        """We want to write if we have received data."""
        response = bool(self.data_to_write)
        self.logger.debug('writable() -> %s', response)
        return response
    
    def handle_write(self):
        """Write as much as possible of the most recent message we have received."""
        data = self.data_to_write.pop()
        #print "hier gaat dus nog iets mis: exceptions.TypeError > object cannot be interpreted as an index ----"
        if data:
            self.queue.put(data) # dit stuur dus bericht geving terug.
            #print "hierooo"
            # sent = self.send(data[:self.chunk_size])   #chunk_size doet dus iets raars...?
            sent = self.send(data[:256])
            # message = self.name + " SAID: " + data#[:-2]
            message = str(data)
            self.logger.debug('Putting data in Queue -> (%s) "%s"', self.name, data)
            try:
                r_server.set("socket",message)
                logger.debug("MSGBUG -> Redis input: %s", message)
                logger.debug("Redis name: %s", self.name)
                r_server.set(self.name,message)
            except:
                logger.warning("ERROR: message name %s", self.name)
                logger.warning("ERROR: message: %s", data)
                logger.warning("MSGBUS failure: verify but exist") # report back vocally ?
                pass
            if sent < len(data):
                remaining = data[sent:]
                try:
                    self.data.to_write.append(remaining)
                    logger.debug("exceptions.AttributeError: EchoHandler instance has no attribute 'data'")
                except:
                    pass
        self.logger.debug('handle_write() -> (%d) "%s"', sent, data[:sent])
        if not self.writable():
            self.handle_close()
        return self.queue

    def handle_read(self):
        data = self.recv(1024) #self.chunk_size) # geen 1024?
        self.logger.debug('handle_read() -> (%d) "%s on BUS: %s"', len(data),data,self.name)
        self.data_to_write.insert(0, data)
        if data:
            self.out_buffer += 'I echo you: ' + data

    def handle_close(self):
        self.logger.debug('handle_close()')
        #self.server.remove_channel(self)
        self.close()

class MessageBus(asyncore.dispatcher):
    # host + port kan dus ook als 1 komen:
    def __init__(self, name, queue):
        #obj = q.get()
        #queue.put(name)
        self.queue = queue
        #obj.do_something()
        self.logger = logging.getLogger()
        self.connections = []
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        host, port = self.check(name)
        #print host,port
        #try:  # sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  ???
        self.bind((host, port))
        # except [error: [Errno 98] Address already in use]
        self.name = name
        # self.address = self.socket.getsockname() # alleen als nodig?
        self.logger.debug('binding to %s', name)
        self.listen(5)
        return

    def check(self,name):
        # This SHOULD check if this is the first BUS, if not, which is the last bus.
        # Starting points should be defined in config file.
        newname = name + "bus"
        if(name == "main"):
            port = r_server.get("mainport")
            r_server.set("lastport",8080)
            r_server.rpush("bus", newname)
            r_server.set(newname,port)
        else:
            r_server.rpush("bus", newname)
            logger.debug("Bus with name: %s", name)
            port = int(r_server.get("lastport")) + 1
            logger.debug("Component: %s got port: %s", name,port)
            r_server.set("lastport",port)
        host = socket.gethostname()
        self.logger.debug('MessageBus Created -> %s on: %s : %s', name, host, port)
        address = (host,int(port))
        r_server.set(newname,int(port))
        return address

    def handle_accept(self):
        client_info = self.accept()
        if client_info:
            self.logger.debug('handle_accept() -> %s', client_info[1])
        if client_info is not None:
            self.sock, self.addr = client_info
            self.logger.debug('Incoming connection from IP %s', repr(self.addr))
            #run forever or until it received instructions
            # to stop. 
            #self.handle_close()
            #print self.name
            handler = EchoHandler(self.queue,self.name, self.sock, self)
            self.connections.append(self.sock)
            # via handler dus...
            
    def handle_close(self):
        # cleaning up connections
        try:
            self.logger.debug('handle_close()')
            self.logger.debug('Disconnected from %s', self.getpeername())
            one = self.getpeername()
            del identity[one]
            del clients[one]
            every=clients.values()
            try:    
                for one in every:
                    one.send('server message:'+str(self.addr)+' quit'+'\n')
            except: pass
        except: pass

    def remove_channel(self, sock):
        if sock in self.connections:
            self.connections.remove(sock)
