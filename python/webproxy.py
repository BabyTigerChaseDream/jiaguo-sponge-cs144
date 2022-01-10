#coding:utf-8
from socket import *
import sys

# function to parse server and path 
# (desthost, destfile)
def extractServerpath(get_url):
    print("extractServerPath , raw get_url", get_url)
    hosturl = get_url.split(' ')[1]
    print('[hosturl]:',hosturl)

    # path parser : TBD
    #print('hosturl split:',hosturl.split('/')[1:])
    print('hosturl split:',hosturl.split('/'))
    hosturl = [x for x in hosturl.split('/') if x and 'http' not in x]
    #desthost, destfile = dest_path[1:].split('/')[0],dest_path[1:].split('/')[2]
    print("*** extractServerpath: ",hosturl, "****\n")
    return hosturl

if len(sys.argv) <= 1:
    print('Usage:"python3 webproxy.py proxyaddr"\n\
            proxyaddr: address of proxy server\n')
    sys.exit(2)

proxyaddr = sys.argv[1]

# create socket, webproxy is playing server role  
proxyservport = 9925 
remotePort = 80
proxyservsocket = socket(AF_INET, SOCK_STREAM)
# fix 'Port' already in use error, due to improper quit of connections
proxyservsocket.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
# Prepare a server socket
proxyservsocket.bind((proxyaddr, proxyservport))
proxyservsocket.listen(5)

#request_url = sys.argv[1]
#request_url in format : 'http://cs144.keithw.org/hello'

while True:
    # localhost request act as a client of proxy
    print('Ready to serve...')
    clisocket, addr = proxyservsocket.accept()
    print('Received a connection from: ', addr)
    request_url = clisocket.recv(4096).decode()
    print('[RAW request to my webproxy],',request_url)
    
    # parse local request - desthost , remotepath
    dest_url = request_url.split('\r\n')[0]
    serverpath = extractServerpath(dest_url)
    print('[calling seeverpath],',serverpath)
    if len(serverpath) == 1:
        desthost = serverpath[0]
        destfile = ''
    elif len(serverpath) == 2:
        desthost, destfile = serverpath
    else:
        raise ValueError("UNexpected serverpath len : ", serverpath)

    #print("dest_url:",dest_url)
    #print("dest_path:",dest_path)
    #print("desthost:",desthost)
    #print("destfile:",destfile)
    #print("\n")

    # check if cache exists
    fileExist = "false"
    try:
        # check if file already in proxy cache 
        f = open(destfile, "r")
        outputdata = f.readlines()
        fileExist = "true"
        print('[log] File Exists!')
        # read file in webproxy local cache  
        for i in range(0, len(outputdata)):
            clisocket.send(outputdata[i].encode())
        print('[log] Read from cache')
    # file not cached , needs to ask for real server
    except IOError:
        print('File Exist ? >>> ', fileExist)
        if fileExist == "false":
            # create socket, webproxy is playing client role  
            print('[log] Creating socket on proxyserver')
            realsocket = socket(AF_INET, SOCK_STREAM)
            print('[log] Host Name: ', desthost)
            # header / msg in http
            # directly send raw_request to real remote server 

            #message='''GET /{path} HTTP/1.1\r\nConnection: {connectiontype}\r\nHost: {remoteserver}:{port}\r\n\r\n'''.format(
            #    path=destfile,
            #    connectiontype='keep-alive',
            #    remoteserver=desthost,
            #    port=80
            #)

            message = request_url 

            print('[WebProxy revised message ]',message)
            try:
                # webproxy is act as a client to remote socket 
                realsocket.connect((desthost, remotePort))
                print('Socket connected to port {remotePort} of the host:{desthost}'.format(desthost=desthost,remotePort=remotePort))
                realsocket.sendall(message.encode())
                # Read the response into buffer
                buff = realsocket.recv(4096)
                print('[buff decode from origin server]',buff.decode())
                # webproxy still acting as a server to send realsocket response to localhost socket
                clisocket.sendall(buff)
                # Create a new file in the cache for the requested file.
                # Also send the response in the buffer to client socket
                # and the corresponding file in the cache
                if destfile:
                    tmpFile = open("./" + destfile, "w")
                    tmpFile.writelines(buff.decode().replace('\r\n', '\n'))
                    tmpFile.close()
                else:
                    print("NO destfile .. skip temFile writting\n ")
            except Exception as e:
                print("Illegal request with error :",e)
        else:
            # HTTP response message for file not found
            # Do stuff here
            print('File Not Found...Stupid Andy')
    # Close the client and the server sockets
    clisocket.close()
proxyservsocket.close()