import time
import socket

TCP_IP = '192.168.0.102'
TCP_PORT = 5005

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

print 'Sending...'
while(1):
    print 'test'
    s.send('test')
    time.sleep(0.01)
print 'Done sending.'
time.sleep(30)
