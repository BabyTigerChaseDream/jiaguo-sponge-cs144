from socket import * 
import base64 
import time 
import ssl

def msgwrapper(msg):
    return msg+'\r\n'

class Email:
    def __init__(self, mailserver='smtp.gmail.com', mailport=587):
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
        self.uname = 'scarlettdiudiu@gmail.com'
        self.pwd = '*****you#guess'
        # receiver info 
        #self.rcptname='scarlettdiudiu@gmail.com'
        self.rcptname='ronl76065@gmail.com'

    def infoEncode(self, uname=None,  pwd=None):
        if not uname:
            uname=self.uname
        if not pwd:
            pwd= self.pwd
        # user account info
        self.enuname=base64.b64encode(uname.encode()).decode() 
        self.enpwd=base64.b64encode(pwd.encode()).decode() 

    def connect(self):
        self.csocket = socket(AF_INET, SOCK_STREAM) 
        self.csocket.connect((self.mailserver,self.mailport)) 
        recv=self.csocket.recv(1024).decode() 
        if recv[:3] != '220':
            # expect msg below
            #'220 163.com Anti-spam GT for Coremail System (163com[20141201])\r\n' 
            print(recv)
            raise ValueError('220 reply not received from server.')

    def sendhelo(self, nickname='JiaJia'):
        self.heloMsg = self.helo.format(user=nickname)
        # messages' template 
        self.csocket.send(self.heloMsg.encode()) 
        recv=self.csocket.recv(1024).decode() 
        if recv[:3] != '250':
            #'250 OK\r\n' 
            print(recv)
            raise ValueError('250 reply not received from server.')
        print(recv)

    def starttls(self):
        temp='STARTTLS\r\n'
        print(temp)
        self.csocket.send(temp.encode())
        recv = self.csocket.recv(1024).decode()
        print(recv)
        self.ssl_csocket= ssl.wrap_socket(self.csocket, ssl_version=ssl.PROTOCOL_SSLv23)

    def authlogin(self):
        self.ssl_csocket.send(self.authMsg.encode()) 
        recv=self.ssl_csocket.recv(1024).decode() 
        if recv[:3] != '334':
            #'334 dXNlcm5hbWU6\r\n' 
            print(recv)
            raise ValueError('334 reply not received from server.')
        print(recv)
        self.ssl_csocket.sendall((self.enuname + '\r\n').encode()) 

        recv=self.ssl_csocket.recv(1024).decode() 
        if recv[:3] != '334':
            #'334 UGFzc3dvcmQ6\r\n' 
            print(recv)
            raise ValueError('334 reply not received from server.')
        self.ssl_csocket.sendall((self.enpwd + '\r\n').encode()) 
        recv=self.ssl_csocket.recv(1024).decode() 
        print(recv)

    def sendmail(self,rcptname=None):
        if not rcptname:
            rcptname =  self.rcptname
        #'235 Authentication successful\r\n' 
        self.mailFromMsg = self.mailFrom.format(uname=self.uname)
        self.ssl_csocket.send(self.mailFromMsg.encode()) 
        recv=self.ssl_csocket.recv(1024).decode() 
        print(recv)
        #'250 Mail OK\r\n' 
        self.rcptToMsg = self.rcptTo.format(rname=rcptname)
        self.ssl_csocket.send(self.rcptToMsg.encode()) 
        recv=self.ssl_csocket.recv(1024).decode() 
        print(recv)
        self.ssl_csocket.send(self.DataMsg.encode()) 
        recv = self.ssl_csocket.recv(1024) 
        recv = recv.decode() 
        print("After DATA command: "+recv) 

        # start content writing 
        subject = "Subject: Say Hi to mean boss\r\n\r\n" 
        self.ssl_csocket.send(subject.encode()) 

        # attach timestamp 
        date = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime()) 
        date = date + "\r\n\r\n" 
        self.ssl_csocket.send(date.encode()) 

        msg = "hello bg 's SMTP client , working now ha ! "
        msg = msg + "\r\n\r\n" 
        self.ssl_csocket.send(msg.encode()) 
        endmsg = "\r\n.\r\n" 
        self.ssl_csocket.send(endmsg.encode()) 
        recv_msg = self.ssl_csocket.recv(1024) 
        print(recv)
        print("Response after sending message body:"+recv_msg.decode()) 
        #quit = "QUIT\r\n" 
        #self.ssl_csocket.send(quit.encode()) 

if __name__ == '__main__':
    E = Email()
    E.infoEncode()
    E.connect()
    E.sendhelo()
    E.authlogin()
    E.sendmail()