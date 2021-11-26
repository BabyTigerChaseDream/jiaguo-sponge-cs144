import socket
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
    print("sentense",sentence.split())
    try:
        output = 'Thank you for connecting'
        header = 'HTTP/1.1 200 OK \nConnection: close\n' + \
        'Content0Length: {}\n'.format(len(output)) + \
        'Content-Type: text/html\n\n'
        connectionSocket.send(header.encode())
        connectionSocket.send(output.encode())
        connectionSocket.close()
    except IOError:
        header = 'HTTP/1.1 404 Not Found'
        connectionSocket.send(header.encode())
        connectionSocket.close()