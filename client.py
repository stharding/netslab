#!/usr/bin/env python
import random, string, sys, socket, hashlib

debug = False

def rand_string( len ):
  str = ''.join(random.choice(string.letters + string.digits) 
    for x in range(len))
  return str

def main():
  global debug
  length = 1000000
  if len(sys.argv) > 1:
    length = int(sys.argv[1])
  if len(sys.argv) > 2:
    debug = True
  msg = rand_string( length )
  hsh = hashlib.md5(msg).hexdigest()
  # if debug: print msg
  if debug: print "Connecting to server ...."
  try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("10.59.1.2", 8888))
    sock.send( str(len(msg)) )
    srvlen = sock.recv( 1024 )
    if debug: print "Got: " + srvlen
    srvlen = int(srvlen)
    if length != srvlen:
      print "ERROR! length and server length differ!"
      exit(-1)
    sock.send( msg )
    reply = sock.recv(1024)
    if debug: print "reply:      " + reply
    if debug: print "MD5 of msg: " + hsh
    if hsh != reply:
      print "ERROR! hash and server hash differ!"
      exit(-2)
  except Exception as e:
    print "got error! ", e
  

if __name__ == '__main__':
  main()
