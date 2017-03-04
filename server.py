import time
import socket

TCP_IP = ""
TCP_PORT = 5005

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(5)

while True:
    conn, addr = s.accept()
    print "Got connection from", addr
    print "Receiving..."
    l = conn.recv(4)
    while (l):
        print "Receiving Data..."
        print l
        l = conn.recv(4)
        print "Done Receiving"
    f.close()
    conn.close()
