from socket import *
import sys 

#host = 'localhost'
#serverPort = 50007 

host = 'cs144.keithw.org'
serverPort = 80 
filename = 'hello'

#filename=sys.argv[1]
# optional 
#serverName=sys.argv[2] or host#sever name,here is my ip address
#serverPort=int(sys.argv[3]) or serverPort #any port consistent with the server end

with socket(AF_INET, SOCK_STREAM) as s:
    s.connect((host, serverPort))
    request_header_1='GET /'
    #request_header_2='''
    #            HTTP/1.1\r\nHost:{host}:{serverPort}\r\nConnection: keep-alive\r\n 
    #                Content-Type: text/html\r\n\r\n'''.format(host=host,serverPort=serverPort)
    #header=request_header_1+filename+' '+request_header_2
    header= '''
        GET /hello HTTP/1.1\r\nHost: {host}\r\n\r\n
    '''.format(host=host)

    #s.sendall(b'Hello, world')
    s.send(header.encode())
    #s.send('hello'.encode())
    data = s.recv(1024)

print('Received', repr(data))