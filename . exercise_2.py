import re,os
import sys
from socket import *
from select import *

class WebServer:
    def __init__(self,host="0.0.0.0",port=80,html=None):
        self.host=host
        self.port=port
        self.html=html
        self.crate_socket()
        self.bind()
    def crate_socket(self):
        self.sockfd=socket()
        self.sockfd.setblocking(False)
    def bind(self):
        self.address=(self.host,self.port)
        self.sockfd.bind(self.address)

    def start(self):
        self.sockfd.listen(5)
        self.ep=epoll()
        self.map={self.sockfd.fileno():self.sockfd}
        self.ep.register(self.sockfd,EPOLLIN)
        while True:
            events=self.ep.poll()
            for fd,enevt in events:
                if fd ==self.sockfd.fileno():
                    connfd,addr=self.map[fd].accept()
                    print("Connect from", addr)
                    connfd.setblocking(False)
                    self.map[connfd.fileno()]=connfd
                    self.ep.register(connfd, EPOLLIN)
                else:
                    try:
                        self.handle(fd)
                    except:
                        self.ep.unregister(fd)
                        self.map[fd].close()
                        del self.map[fd]

    #处理客户端请求
    def handle(self,fd):
        request = self.map[fd].recv(1024 * 10).decode()
        pattern=r"[A-Z]+\s+(?P<info>/\S*)"
        result=re.match(pattern,request)
        print(request)
        print(result)
        if result:
            info=result.group("info")
            print("请求的内容：",info)
            self.send_response(fd, info)
        else:
            self.ep.unregister(fd)
            self.map[fd].close()
            del self.map[fd]
            return


    def send_response(self,fd,info):
        if info =="/":
            filename=self.html + "/index.html"
        else:
            filename=self.html + info

        try:
            file=open(filename,"rb")

        except:
            response = "HTTP/1.1 404 Not found\r\n"
            response += "Content-Type:text/html\r\n"
            response += "\r\n"
            response += "404 Not found"
            response = response.encode()

        else:
            data=file.read()
            response = "HTTP/1.1 200 OK\r\n"
            response += "Content-Type:text/html\r\n"
            response += "Content-Length:%d\r\n"%(len(data))
            response += "\r\n"
            response = response.encode()+ data
        finally:
            self.map[fd].send(response)




if __name__ == '__main__':
    httpd=WebServer(host="0.0.0.0",port=8001,html="./static")
    httpd.start()
    ***********************************************************
