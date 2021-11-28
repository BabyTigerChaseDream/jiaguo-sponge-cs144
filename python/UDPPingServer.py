import random
from socket import *

# Create UDP socket
# Notice the use of SOCK_DGRAM for UDP packets

serverSocket = socket(AF_INET, SOCK_DGRAM)
# assign IP address and port number to socket 
serverSocket.bind(('',12000))

while True:
    # Generate random number in the range of 0-10
    rand = random.randint(0,10)
    # receive the client packet along with the address it is coming from 
    message, address = serverSocket.recvfrom(1024)
    #Capitalize the message from the client 
    message = message.upper()

    # if rand is less then 4 , we consider the packet list and do not response
    print('[rand is：',rand)
    if rand > 4:
	    continue
    # Otherwise , the server responds
    serverSocket.sendto(message, address)