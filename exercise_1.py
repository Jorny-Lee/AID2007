import sys
from socket import *
sockfd=socket()
sockfd.bind(("0.0.0.0",8000))
sockfd.listen(5)

#接收到的是来自浏览器的HTTP请求
while True:
    try:
        connfd, addr = sockfd.accept()
        print("Connect from", addr)
    except KeyboardInterrupt:
        sys.exit("服务退出")
    data=connfd.recv(1024*10).decode()
    if not data:
        continue
    content=data.split(" ")[1]
    print(content)
    if content=="/first.html":
        with open("first.html","r") as f:
            data=f.read()
        response="HTTP/1.1 200 OK\r\n"
        response+="Content-Type:text/html\r\n"
        response+="\r\n"
        response=response+data

    else:
        response = "HTTP/1.1 404 Not found\r\n"
        response += "Content-Type:text/html\r\n"
        response += "\r\n"
        response += "404 Not found"
    connfd.send(response.encode())
connfd.close()
sockfd.close()