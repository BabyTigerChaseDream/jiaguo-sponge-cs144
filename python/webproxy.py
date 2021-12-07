#coding:utf-8
from socket import *
import sys

if len(sys.argv) <= 1:
    print('Usage:"python3 webproxy.py request_url"\n\
            request_url: full url of proxy server\n')
    sys.exit(2)

request_url = sys.argv[1]
#request_url in format : 'localhost:9925/http://cs144.keithw.org/hello'
print('[reques_url],',request_url)

# create socket, webproxy is playing server role  
proxyservport = 9925 
proxyservsocket = socket(AF_INET, SOCK_STREAM)

# fix 'Port' already in use error, due to improper quit of connections
proxyservsocket.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)

# Prepare a server socket
proxyservsocket.bind(('', proxyservport))
proxyservsocket.listen(5)

while True:
    # localhost request act as a client of proxy
    print('Ready to serve...')
    clisocket, addr = proxyservsocket.accept()
    print('Received a connection from: ', addr)
    #request_url = clisocket.recv(4096).decode()

    # 从请求中解析出filename
    org_file_path= request_url.partition("//")[-1]
    filename = org_file_path.partition("/")[-1]
    print("[org_file_path] ",org_file_path)
    print("[filename] ",filename)
    fileExist = "false"
    try:
        # check if file already in proxy cache 
        f = open(filename, "r")
        outputdata = f.readlines()
        fileExist = "true"
        print('File Exists!')

        # read file in webproxy local cache  
        for i in range(0, len(outputdata)):
            clisocket.send(outputdata[i].encode())
        print('Read from cache')

    # file not cached , needs to ask for real server
    except IOError:
        print('File Exist ? >>> ', fileExist)
        if fileExist == "false":
            # create socket, webproxy is playing client role  
            print('Creating socket on proxyserver')
            realsocket = socket(AF_INET, SOCK_STREAM)

            remotehost = org_file_path.partition("/")[0]
            print('Host Name: ', remotehost)

            # header messages in http
            # fake remotehost
            remotehost = 'localhost'
            request_header_1='GET /'
            request_header_2='''
                        HTTP/1.1\nHost:{host}:{serverPort}\r\nConnection: keep-alive\n 
                            Content-Type: text/html\r\n'''.format(host=remotehost,serverPort=80)
            message=request_header_1+filename+request_header_2
            
            try:
                # webproxy is act as a client to remote socket 

                realsocket.connect((remotehost, 80))
                print('Socket connected to port 80 of the host:{remotehost}'.format(remotehost=remotehost))

                realsocket.sendall(message.encode())
                # Read the response into buffer
                buff = realsocket.recv(4096)
                print('[buff decode from origin server]',buff.decode())
                # webproxy still acting as a server to send realsocket response to localhost socket
                clisocket.sendall(buff)
                # Create a new file in the cache for the requested file.
                # Also send the response in the buffer to client socket
                # and the corresponding file in the cache
                tmpFile = open("./" + filename, "w")
                tmpFile.writelines(buff.decode().replace('\r\n', '\n'))
                tmpFile.close()

            except Exception as e:
                print("Illegal request with error :",e)

        else:
            # HTTP response message for file not found
            # Do stuff here
            print('File Not Found...Stupid Andy')
    # Close the client and the server sockets
    clisocket.close()
proxyservsocket.close()