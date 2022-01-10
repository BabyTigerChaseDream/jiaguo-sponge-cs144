from socket import * 
import base64 
import time 
import ssl

# Notes: 
# remember to turn on 'less secure mode' in gmail account settings

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
        self.rcptname='scarlettdiudiu@gmail.com'
        #self.rcptname='ronl76065@gmail.com'

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

        msg = "hello Email attachment client , working now ha ! "
        msg = msg + "\r\n\r\n" 
        self.ssl_csocket.send(msg.encode()) 

        ################################################
        # add attachment 
        '''
        #send_text_with_image='from:%s\nto:%s\nsubject:hello,you!\
        send_text_with_image='subject:hello,you!\
        \nContent-Type:multipart/mixed;boundary="simple"\n\n--simple\n\n'
        send_text_with_image=send_text_with_image.encode()+'Content-Type:image/JPEG\nContent-transfer-encoding:base64\n\n'.encode()
        '''

        send_text_with_image='from:{fromaddr}\nto:{toaddr}\nsubject:hello,image !\
        \nContent-Type:multipart/mixed;boundary="simple"\n\n--simple\n'.format(
        fromaddr=self.uname,toaddr=self.rcptname
        )+'Content-Type:text/html\n\n<h1>hello</h1><img src="https://pic3.zhimg.com/50/v2-29a01fdecc80b16e73160c40637a5e8c_hd.jpg">\n\n'
        send_text_with_image=send_text_with_image.encode()+'--simple\n'.encode()+'Content-Type:image/JPEG\nContent-transfer-encoding:base64\n\n'.encode()
        f=open('ssl_module_openssl.png','rb').read()

        f=base64.b64encode(f)
        send_text_with_image+=f
        send_text_with_image+='\n--simple\r\n'.encode()

        print('[attach img]',send_text_with_image)
        self.ssl_csocket.send(send_text_with_image) 
        recv_msg = self.ssl_csocket.recv(1024) 
        print(recv)
        ################################################
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
    E.starttls()
    E.authlogin()
    E.sendmail()