from socket import *
import os
import json

serverPort = 50007 
serverSocket = socket(AF_INET,SOCK_STREAM)

# fix 'Port' already in use error, due to improper quit of connections
serverSocket.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)

serverSocket.bind(('',serverPort))
serverSocket.listen(1)
print("The server is ready to receive")
while 1:
    connSocket, addr = serverSocket.accept()
    sentence = connSocket.recv(1024)
    # first key:value part in connSocket.recv(1024) is 'GET/POST':(url path)
    print("[received socket data]\n\t",sentence.split()[1],"#\n")
    #print("connSocket,addr,sentense",connSocket,addr,sentence)
    #print("sentense",sentence.split())

    # decode bytes into strings
    filename = sentence.decode().split()[1] 
    print('### Type of filename : ',type(filename))

    try:
        '''
        header = 'HTTP/1.1 200 OK \nConnection: keep-alive\n' + \
        'Content0Length: {}\n'.format("To Be Decided") + \
        'Content-Type: text/html\n\n'
        connSocket.send(header.encode())
        '''

        header_default = 'HTTP/1.1 404 {} Not Found\nContent-Type: text/html\n\n'

        #output = 'Thank you for connecting\n'
        #connSocket.send(output.encode())

        os.system('pwd')
        cwd = os.getcwd()
        filename_cwd = cwd + filename
        reply = 'empty\n\r'
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
    except IOError:
        header = header_default.format('nothing on filename')
        connSocket.send(header.encode())
        connSocket.close()