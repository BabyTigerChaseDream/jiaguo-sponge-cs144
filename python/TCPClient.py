import socket
import sys 

host = 'localhost'
serverPort = 50007 

#host = 'cs144.keithw.org'
#serverPort = 80 

filename=sys.argv[1]
# optional 
#serverName=sys.argv[2] or host#sever name,here is my ip address
#serverPort=int(sys.argv[3]) or serverPort #any port consistent with the server end

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, serverPort))
    request_header_1='GET /'
    request_header_2='''
                HTTP/1.1\nHost:{host}:{serverPort}\r\nConnection: keep-alive\n 
                    Content-Type: text/html\r\n'''.format(host=host,serverPort=serverPort)
    header=request_header_1+filename+request_header_2

    #s.sendall(b'Hello, world')
    s.send(header.encode())
    s.send('TCPClient.py'.encode())
    data = s.recv(1024)

print('Received', repr(data))