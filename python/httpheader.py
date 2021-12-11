 #msg template:
# path : hello
# connectiontype : close/keep-alive
# remoteserver : cs144.keithw.org 
# port(optional) : 80

msg='''GET /{path} HTTP/1.1\r\nConnection: {connectiontype}\r\nHost: {remoteserver}:{port}\r\n\r\n'''


from socket import *
s=socket(AF_INET, SOCK_STREAM)
s.connect(('cs144.keithw.org',80))

msg='''GET /hello HTTP/1.1\r\nConnection: close\r\nHost: cs144.keithw.org\r\n\r\n'''
s.send(msg.encode())
s.recv(1024)
#b'HTTP/1.1 200 OK\r\nDate: Sat, 11 Dec 2021 00:55:15 GMT\r\nServer: Apache\r\nLast-Modified: Thu, 13 Dec 2018 15:45:29 GMT\r\nETag: "e-57ce93446cb64"\r\nAccept-Ranges: bytes\r\nContent-Length: 14\r\nConnection: close\r\nContent-Type: text/plain\r\n\r\nHello, CS144!\n'

s=socket(AF_INET, SOCK_STREAM)
s.connect(('cs144.keithw.org',80))
msg='''GET /hello HTTP/1.1\r\nConnection: close\r\nHost: cs144.keithw.org:80\r\n\r\n'''
s.send(msg.encode())
s.recv(1024)
#b'HTTP/1.1 200 OK\r\nDate: Sat, 11 Dec 2021 00:56:25 GMT\r\nServer: Apache\r\nLast-Modified: Thu, 13 Dec 2018 15:45:29 GMT\r\nETag: "e-57ce93446cb64"\r\nAccept-Ranges: bytes\r\nContent-Length: 14\r\nConnection: close\r\nContent-Type: text/plain\r\n\r\nHello, CS144!\n'

msg='''GET /hello HTTP/1.1\r\nConnection: keep-alive\r\nHost: cs144.keithw.org:80\r\n\r\n'''
s=socket(AF_INET, SOCK_STREAM)
s.connect(('cs144.keithw.org',80))
s.send(msg.encode())
s.recv(1024)
#b'HTTP/1.1 200 OK\r\nDate: Sat, 11 Dec 2021 00:57:16 GMT\r\nServer: Apache\r\nLast-Modified: Thu, 13 Dec 2018 15:45:29 GMT\r\nETag: "e-57ce93446cb64"\r\nAccept-Ranges: bytes\r\nContent-Length: 14\r\nKeep-Alive: timeout=30, max=100\r\nConnection: Keep-Alive\r\nContent-Type: text/plain\r\n\r\nHello, CS144!\n'

s=socket(AF_INET, SOCK_STREAM)
s.connect(('cs144.keithw.org',80))
msg='''GET /hello HTTP/1.1\r\nHost: cs144.keithw.org:80\r\n\r\n'''
s.send(msg.encode())
s.recv(1024)
#b'HTTP/1.1 200 OK\r\nDate: Sat, 11 Dec 2021 01:12:29 GMT\r\nServer: Apache\r\nLast-Modified: Thu, 13 Dec 2018 15:45:29 GMT\r\nETag: "e-57ce93446cb64"\r\nAccept-Ranges: bytes\r\nContent-Length: 14\r\nContent-Type: text/plain\r\n\r\nHello, CS144!\n'

s=socket(AF_INET, SOCK_STREAM)
s.connect(('cs144.keithw.org',80))
msg='''GET /hello HTTP/1.1\r\nHost: cs144.keithw.org\r\n\r\n'''
s.send(msg.encode())
s.recv(1024)
#b'HTTP/1.1 200 OK\r\nDate: Sat, 11 Dec 2021 01:12:52 GMT\r\nServer: Apache\r\nLast-Modified: Thu, 13 Dec 2018 15:45:29 GMT\r\nETag: "e-57ce93446cb64"\r\nAccept-Ranges: bytes\r\nContent-Length: 14\r\nContent-Type: text/plain\r\n\r\nHello, CS144!\n'
