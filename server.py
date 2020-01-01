import socket
import threading
import msgList
import queue
import json
import os
import sys
import time

USER_POOL = []
onlineList = []
LOGIN_NAME_LIST = []#only login nickname
lock = threading.Lock()
msgque = queue.Queue()#msg queue
port = 7799
file_port = 22333


class Chat(threading.Thread):
    def __init__(self,port):
        threading.Thread.__init__(self)
        self.sock = ('',port)
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    
    def run(self):
        self.socket.bind(self.sock)
        self.socket.listen(16)
        send = threading.Thread(target=self.senddata)
        send.start()
        while True:
            client,clientSock = self.socket.accept()
            t = threading.Thread(target=self.tcp_connect,args=[client])
            USER_POOL.append(t)#客户加入线程池
            t.start()
                

    def tcp_connect(self,client):
        while True:
            (status,username) = self.try_login(client)
            if status == "succ":
                try:
                    while True:
                        recv_data = client.recv(1024)
                        recv_data = json.loads(recv_data.decode())
                        
                        if (recv_data['type'] == 'USER_MSG_ALL'):
                            data = ("ALL", recv_data['message'], "USER_MSG", recv_data['sender'], recv_data['send_time'])
                            print(recv_data['sender'])
                            self.putMsgToQue(data)

                        elif (recv_data['type'] == 'USER_PIC_ALL'):
                            print(recv_data['sender'])

                            imgdata = client.recv(40960000)
                            data = ("ALL", imgdata, "USER_PIC", recv_data['sender'], recv_data['send_time'])
                            self.putMsgToQue(data)

                        elif (recv_data['type'] == 'USER_MSG_PRI'):
                            data = ("PRI", recv_data['message'], "USER_MSG", recv_data['sender'], recv_data['send_time'],recv_data['tolist'])
                            print(recv_data['sender'])
                            self.putMsgToQue(data)

                        elif (recv_data['type'] == 'USER_PIC_PRI'):
                            print(recv_data['sender'])

                            imgdata = client.recv(40960000)
                            data = ("PRI", imgdata, "USER_PIC", recv_data['sender'], recv_data['send_time'],recv_data['tolist'])
                            self.putMsgToQue(data)



                except:
                    print(username,'Disconnect')
                    index = 0
                    for user in onlineList:
                        if user[0] == client:
                            global LOGIN_NAME_LIST
                            onlineList.pop(index)#将此用户移除在线用户列表
                            LOGIN_NAME_LIST = self.flushUsernames()#刷新用户名列表
                            USER_POOL.pop(index)
                            data = ("ALL", LOGIN_NAME_LIST, "USERNAME_LIST")
                            self.putMsgToQue(data)#将用户名列表放入消息队列
                        index = index + 1
                    break



    def try_login(self,client_socket):
        global LOGIN_NAME_LIST
        username = client_socket.recv(1024)
        username = username.decode()

        if username:
            print("RECV:",username)
            if len(USER_POOL) >= 16:
                data = (client_socket, msgList.err_service_full, "SERVER_HINT")
                self.putMsgToQue(data)
                return ("fail","")
            elif username in LOGIN_NAME_LIST:
                data = (client_socket, msgList.err_existedNickName, "SERVER_HINT")
                self.putMsgToQue(data)
                return ("fail","")
            #can login
            else:
                onlineList.append((client_socket, username))
                LOGIN_NAME_LIST = self.flushUsernames()
                data = (client_socket, msgList.login_succ, "SERVER_HINT")
                self.putMsgToQue(data)

                data = ("ALL",LOGIN_NAME_LIST,"USERNAME_LIST")
                self.putMsgToQue(data)

                time.sleep(0.2)
                listdir = os.listdir(os.getcwd())
                data = ("ALL",listdir,"FILE_LIST")
                self.putMsgToQue(data)

                return ("succ",username)
    
    #Update LOGIN_NAME_LIST
    def flushUsernames(self):
        LOGIN_NAME_LIST = []
        for i in onlineList:
            LOGIN_NAME_LIST.append(i[1])
        return LOGIN_NAME_LIST

    def putMsgToQue(self,msg):
        lock.acquire()
        try:
            msgque.put(msg)
        finally:
            lock.release()

    #send msg while msg_queue not empty
    def senddata(self):
        messageaH = {}
        while True:
            if not msgque.empty():
                message = msgque.get()
                if message[2] == "SERVER_HINT":
                    messageaH = {'type':'SERVER_HINT','message':message[1]}
                    message[0].send(json.dumps(messageaH).encode())
                    continue
                
                elif message[2] == "USERNAME_LIST":
                    messageaH = {'type':'onlineList','message':message[1]}

                elif message[2] == "FILE_LIST":
                    messageaH = {'type':'fileList','message':message[1]}
            
                elif message[2] == "USER_MSG":
                    messageaH = {'type':'USER_MSG','message':message[1],'sender':message[3],'send_time':message[4]}

                elif message[2] == "USER_PIC":
                    messageaH = {'type':'USER_PIC','sender':message[3],'send_time':message[4]}

                for user in onlineList:
                    try:
                        print(messageaH)
                        if message[0] == "ALL":

                            if message[2] == "USER_PIC":
                                user[0].send(json.dumps(messageaH).encode())
                                user[0].sendall(message[1])

                            else:
                                user[0].send(json.dumps(messageaH).encode())
                                
                        else:
                            if user[1] in message[-1] or user[1] == message[3]:

                                if message[2] == "USER_PIC":
                                    user[0].send(json.dumps(messageaH).encode())
                                    user[0].sendall(message[1])

                                else:
                                    user[0].send(json.dumps(messageaH).encode())
                    except:
                        print('no user or message to send')



class FileServer(threading.Thread):
    def __init__(self, port):
        threading.Thread.__init__(self)
        self.port = port
        self.sock = ('', port)
        os.chdir(sys.path[0])
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.path = r".\UploadFile"
        os.chdir(self.path)
    
    def run(self):
        print('File server starts running...')
        self.socket.bind(("",self.port))
        self.socket.listen(3)
        while True:
            client, clientSock  = self.socket.accept()
            t = threading.Thread(target=self.tcp_connect, args = [client])
            t.start()
        self.socket.close()
    
    def tcp_connect(self, client):
        while True:
            recv_data = client.recv(1024)
            recv_data = json.loads(recv_data.decode())
            self.recv_func(recv_data['type'], recv_data['message'], client)

        client.close()
    
    def recv_func(self, order, message, client):
        if order == 'DOWNLOAD':
            return self.sendFile(message, client)
        elif order == 'UPLOAD':
            fileName = r'./' + message
            return self.recvFile(fileName, client)
        elif order == 'REQUEST_FILE_LIST':
            pass
    
    def recvFile(self, file_path, client):
            with open(file_path, 'wb') as f:
                while True:
                    data = client.recv(1024)
                    if data == 'EOF'.encode():
                        break
                    f.write(data)
    
    def sendFile(self, fileName, client):
        f = open(fileName, 'rb')
        while True:
            a = f.read(1024)
            if not a:
                break
            client.send(a)
        time.sleep(0.1)
        client.send('EOF'.encode())







#Program starts here!
#chat file 使用不同的sock连接
chatserver = Chat(port)
chatserver.start()
fserver = FileServer(file_port)
fserver.start()

number = len(LOGIN_NAME_LIST)
while number != len(LOGIN_NAME_LIST):
    print(LOGIN_NAME_LIST)
