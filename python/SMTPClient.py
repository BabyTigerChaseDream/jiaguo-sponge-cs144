from socket import * 
import base64 
import time 

def msgwrapper(msg):
    return msg+'\r\n'

def Email(self):
    def __init__(self, mailserver='smtp.163.com', mailport=25):
        # constant of Email client  
        self.mailserver = mailserver
        self.mailport = mailport
        # message template 
        self.authMsg = msgwrapper('AUTH LOGIN')
        self.helo = msgwrapper('HELO {user}')
        self.mailFrom = msgwrapper("MAIL FROM:<{uname}>")
        self.rcptTo= msgwrapper("RCPT TO:<{rname}>")
        self.DataMsg = msgwrapper("DATA")

        # email info 
        self.rcptname='codingmylife0925@163.com'

    def infoEncode(self, uname='codingmylife0925@163.com',  pwd='GLFALBFKQUBTPFQT'):
        # user account info
        self.enuname=base64.b64encode(uname.encode()).decode() 
        self.enpwd=base64.b64encode(pwd.encode()).decode() 

    def connect(self):
        self.csocket = socket(AF_INET, SOCK_STREAM) 
        self.csocket.connect((self.mailserver,self.mailport)) 
        recv=clientSocket.recv(1024).decode() 
        # expect msg below
        #'220 163.com Anti-spam GT for Coremail System (163com[20141201])\r\n' 
        print(recv)

    def helo(self, nickname='JiaJia'):
        self.heloMsg = self.helo.format(user=nickname)
        # messages' template 
        self.csocket.send(self.heloMsg.encode()) 
        recv=self.csocket.recv(1024).decode() 
        print(recv)
        #'250 OK\r\n' 

    def authlogin(self):
        self.csocket.send(self.authMsg.encode()) 
        recv=self.csocket.recv(1024).decode() 
        print(recv)
        #'334 dXNlcm5hbWU6\r\n' 
        self.csocket.sendall((self.enuname + '\r\n').encode()) 
        recv=self.csocket.recv(1024).decode() 
        print(recv)
        #'334 UGFzc3dvcmQ6\r\n' 
        self.csocket.sendall((self.enpwd + '\r\n').encode()) 
        recv=self.csocket.recv(1024).decode() 
        print(recv)

    def sendmail(self,rcptname=None):
        if not rcptname:
            rcptname =  self.rcptname
        #'235 Authentication successful\r\n' 
        self.mailFromMsg = self.mailFrom.format(uname=self.uname)
        self.csocket.send(self.mailFromMsg.encode()) 
        recv=self.csocket.recv(1024).decode() 
        print(recv)
        #'250 Mail OK\r\n' 
        self.rcptToMsg = self.rcptTo.format(uname=rcptname)
        self.csocket.send(self.rcptToMsg.encode()) 
        recv=self.csocket.recv(1024).decode() 
        print(recv)
        self.csocket.send(self.DataMsg.encode()) 
        recv4 = self.csocket.recv(1024) 
        recv4 = recv4.decode() 
        print("After DATA command: "+recv4) 

        # start content writing 
        subject = "Subject: testing my client\r\n\r\n" 
        self.csocket.send(subject.encode()) 

        # attach timestamp 
        date = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime()) 
        date = date + "\r\n\r\n" 
        self.csocket.send(date.encode()) 

        msg = "hello from your SMTP client , JIa "
        msg = msg + "\r\n\r\n" 
        self.csocket.send(msg.encode()) 
        endmsg = "\r\n.\r\n" 
        self.csocket.send(endmsg.encode()) 
        recv_msg = self.csocket.recv(1024) 
        print("Response after sending message body:"+recv_msg.decode()) 
        #quit = "QUIT\r\n" 
        #self.csocket.send(quit.encode()) 

if __name__ == '__main__':
    conn()