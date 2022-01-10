import socket
import os
import json

import threading

def ServerHandler(host='localhost', serverPort=50007, clientmax=1):
    serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    # fix 'Port' already in use error, due to improper quit of connections
    serverSocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

    serverSocket.bind((host,serverPort))
    serverSocket.listen(clientmax)
    print("The mthread server is ready to receive")
    return serverSocket

def clientHander(connSocket,addr):
    try:
        sentence = connSocket.recv(1024)

        # first key:value part in connSocket.recv(1024) is 'GET/POST':(url path)
        print("[received socket data]\n\t",sentence.split()[1],"#\n")
        #print("sentense",sentence.split())

        # decode bytes into strings
        filename = sentence.decode().split()[1] 
        print('### Type of filename : ',type(filename))

        header_default = 'HTTP/1.1 404 {} Not Found\nContent-Type: text/html\n\n'

        os.system('pwd')
        cwd = os.getcwd()
        filename_cwd = cwd + filename
        reply = 'mthread empty\n\r'
        if os.path.isfile(filename_cwd):
            with open(filename_cwd) as f:
                reply = f.read()
            #header = 'HTTP/1.1 200 OK \nConnection: keep-alive\n' + \
            #'Content0Length:<html><body><h4>{}<\h4></body></html>'.format(filename_cwd) + \
            #'Content-Type: text/html\n\n'
            header = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'
        else:
            header = header_default.format(filename_cwd)

        connSocket.send(header.encode())
        connSocket.send(reply.encode())
        connSocket.close()
    except socket.error as socketerror:
        print("Time is UP !!!: ", socketerror)
        connSocket.shutdown(socket.SHUT_RDWR)
        connSocket.close()
    except IOError:
        header = header_default.format('nothing on filename')
        connSocket.send(header.encode())
        connSocket.close()

if __name__=='__main__':
    serverSocket = ServerHandler(host='localhost', serverPort=50007, clientmax=1)
    while 1:
        # received client connections 
        connSocket, addr = serverSocket.accept()
        # start new thread to handle connSocket
        connSocket.settimeout(5)
        threading.Thread(target = clientHander,args = (connSocket, addr)).start()

