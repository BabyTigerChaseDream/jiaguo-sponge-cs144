import socket
import os
import json

serverPort = 50007 
serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# fix 'Port' already in use error, due to improper quit of connections
serverSocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

serverSocket.bind(('',serverPort))
serverSocket.listen(1)
print("The server is ready to receive")
while 1:
    connectionSocket, addr = serverSocket.accept()
    sentence = connectionSocket.recv(1024)
    # first key:value part in connectionSocket.recv(1024) is 'GET/POST':(url path)
    print("[received socket data]\n\t",sentence.split()[1],"#\n")
    #print("connectionSocket,addr,sentense",connectionSocket,addr,sentence)
    #print("sentense",sentence.split())

    # decode bytes into strings
    filename = sentence.decode().split()[1] 
    print('### Type of filename : ',type(filename))

    try:
        header = 'HTTP/1.1 200 OK \nConnection: close\n' + \
        'Content0Length: {}\n'.format("To Be Decided") + \
        'Content-Type: text/html\n\n'
        connectionSocket.send(header.encode())
        output = 'Thank you for connecting\n'
        connectionSocket.send(output.encode())

        os.system('pwd')
        cwd = os.getcwd()
        filename_cwd = cwd + filename
        if os.path.isfile(filename_cwd):
            with open(filename_cwd) as f:
                reply = f.read()
            header = 'HTTP/1.1 200 OK \nConnection: close\n' + \
            'Content0Length: <h4>{}\n<\h4>'.format(filename_cwd) + \
            'Content-Type: text/html\n\n'
        else:
            header = 'HTTP/1.1 404 {} Not Found'.format(filename_cwd)

        connectionSocket.send(header.encode())
        connectionSocket.send(reply.encode())
        connectionSocket.close()
    except IOError:
        header = 'HTTP/1.1 404 ALL Not Found'
        connectionSocket.send(header.encode())
        connectionSocket.close()