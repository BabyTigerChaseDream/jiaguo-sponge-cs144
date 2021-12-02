from socket import * 
import base64 
import time 

def msgwrapper(msg):
    return msg+'\r\n'

class Email:
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
        self.uname = 'codingmylife0925@163.com'
        self.pwd = 'GLFALBFKQUBTPFQT'
        # receiver info 
        self.rcptname='codingmylife0925@163.com'

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

    def authlogin(self):
        self.csocket.send(self.authMsg.encode()) 
        recv=self.csocket.recv(1024).decode() 
        if recv[:3] != '334':
            #'334 dXNlcm5hbWU6\r\n' 
            print(recv)
            raise ValueError('334 reply not received from server.')
        print(recv)
        self.csocket.sendall((self.enuname + '\r\n').encode()) 

        recv=self.csocket.recv(1024).decode() 
        if recv[:3] != '334':
            #'334 UGFzc3dvcmQ6\r\n' 
            print(recv)
            raise ValueError('334 reply not received from server.')
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
        self.rcptToMsg = self.rcptTo.format(rname=rcptname)
        self.csocket.send(self.rcptToMsg.encode()) 
        recv=self.csocket.recv(1024).decode() 
        print(recv)
        self.csocket.send(self.DataMsg.encode()) 
        recv = self.csocket.recv(1024) 
        recv = recv.decode() 
        print("After DATA command: "+recv) 

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
        print(recv)
        print("Response after sending message body:"+recv_msg.decode()) 
        #quit = "QUIT\r\n" 
        #self.csocket.send(quit.encode()) 

if __name__ == '__main__':
    E = Email()
    E.infoEncode()
    E.connect()
    E.sendhelo()
    E.authlogin()
    E.sendmail()