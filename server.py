import socket
import threading
import msgList
import queue
import json

onlineList = [] #在线用户列表，包含用户的sock，ip和端口，以及用户名
LOGIN_NAME_LIST = []#只存放用户名
lock = threading.Lock()#线程锁，防止多个进程将写入数据打乱
msgque = queue.Queue()#消息队列
port =  7798 #服务器端不需要ip地址，使用默认即可

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('',port))
server_socket.listen(128)

USER_POOL = []

class Chat(threading.Thread):
    def __init__(self,port):
        threading.Thread.__init__(self)
        self.sock = ('',port)
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    def tcp_connect(self,client,clientSock):

        username = self.try_login(client,clientSock)
        try:
            while True:
                data = client.recv(1024)
                data = json.loads(data.decode())
                print('receive message',data)
                self.putMsgToQue(data,clientSock)

        except:
            print(username,' 连接断开')
            index = 0
            for user in onlineList:
                if user[0] == client:
                    onlineList.pop(index)#将此用户移除在线用户列表
                    LOGIN_NAME_LIST = self.flushUsernames()#刷新用户名列表
                    self.putMsgToQue(LOGIN_NAME_LIST,clientSock)#将用户名列表放入消息队列
                index = index + 1

    def try_login(self,client_socket,clientSock):
        global LOGIN_NAME_LIST
        username = client_socket.recv(1024)
        username = username.decode()

        if username:
            if len(USER_POOL) >= 128:
                client_socket.send(msgList.err_service_full.encode("utf8"))
            #data = username.decode("utf8")
            if username in LOGIN_NAME_LIST:
                client_socket.send(msgList.err_existedNickName.encode("utf8"))
            else:
                onlineList.append((client_socket, clientSock, username))#添加到在线用户
                LOGIN_NAME_LIST = self.flushUsernames()
                msgque.put(LOGIN_NAME_LIST,client_socket)#将用户名列表放入消息队列
                client_socket.send(msgList.login_succ.encode("utf8"))
                print(LOGIN_NAME_LIST)
                return username
        
    def flushUsernames(self):#将在线用户列表中的用户名刷新到用户名列表
        LOGIN_NAME_LIST = []
        for i in onlineList:
            LOGIN_NAME_LIST.append(i[2])
        return LOGIN_NAME_LIST

    def putMsgToQue(self,msg,clientSock): #将消息和ip以及端口填入队列
        lock.acquire()
        try:
            msgque.put((clientSock, msg))
        finally:
            lock.release()



    def senddata(self):#当队列不为空时发送消息
        while True:
            if not msgque.empty():

                message = msgque.get()
                messageaH = {}
                print(message[1])
                if isinstance(message[1],str):#string
                    print('server send message is string')
                    messageaH = {'type':'message','message':message[1],'username':message[0]}#添加消息说明
                elif isinstance(message[1],list):#list
                    print('server send message is list')
                    messageaH = {'type': 'onlineList', 'userList': message[1]}

                for user in onlineList:
                    try:
                        if isinstance(message[1], str):
                            if user[1] != messageaH['username']:#不给消息发送者转发消息
                                user[0].send(json.dumps(messageaH).encode())
                        else:
                            user[0].send(json.dumps(messageaH).encode())
                    except:
                        print('no user or message to send')



    def run(self):
        self.s.bind(self.sock)
        self.s.listen(5)
        send = threading.Thread(target=self.senddata)
        send.start()
        while True:
            client,clientSock = self.s.accept()
            t = threading.Thread(target=self.tcp_connect,args=[client,clientSock])
            USER_POOL.append(t)#客户加入线程池
            t.start()


while True:
    #chat file 使用不同的sock连接

    chatserver = Chat(port)
    chatserver.start()