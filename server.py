#!/usr/bin/env python

import socket, threading, hashlib, sys

debug = False

class Client(threading.Thread):
  def __init__(self, sock, addr):
    threading.Thread.__init__(self)
    self.socket = sock
    self.address = addr

  def run(self):
    message = ''  
    try:
      length = self.socket.recv(1024)
      if debug: print "lenght is " + length
      
      self.socket.send( length )
      length = int(length)

      while len(message) < length:  
        msg = self.socket.recv(64)
        if msg == '': 
          if debug: print "should be done!!"
          break
        message += msg
      if debug: print message
      hsh = hashlib.md5(message).hexdigest()
      self.socket.send( hsh )
      self.socket.close()
    except KeyboardInterrupt:
      print "got an interupt in the Client class"
      self.socket.close()
    except socket.error as err:
      print "Got error", err
      self.socket.close()

def main():
  global debug
  if len(sys.argv) > 1: debug = True
  host = "10.59.1.2"
  port = 8888
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  sock.bind((host, port))
  sock.listen(64)  
  
  while(True):
    client_sock, addr = sock.accept()
    t = Client(client_sock, addr)
    t.start()
    
  sock.close()

if __name__ == "__main__":
    main()
