# optional heartbeat program
from socket import *
import time
servername='127.0.0.1'
serverPort=800
clientSocket=socket(AF_INET,SOCK_DGRAM)

#clientSocket.settimeout(0.1)

for i in range(1,5):
#for i in range(1,11):
    stime=time.time()
    message=str(i)+' '+str(time.time())

    # trial : send headers to socket , it just display a string sent from client 
    #message = '''
    #    HTTP/1.1\nHost:{servername}:{serverPort}\r\nConnection: keep-alive\n 
    #        Content-Type: text/html\r\n
    #'''
    clientSocket.sendto(message.encode(),(servername,serverPort))

    try:
        print('[waiting for server to send close]', message)
        message, address = clientSocket.recvfrom(1024)
        message=message.decode()
        print('[client received]', message)
        #clientSocket.close()
    except socket.timeout:
        print('REQUEST TIMED OUT')