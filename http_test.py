"""
http请求响应示例
"""
from socket import *
sock=socket()
sock.bind(("0.0.0.0",8000))
sock.listen(5)

#浏览器输入地址后会自动连接服务端
connfd,addr=sock.accept()
print("Connect from",addr)
#接收到的是来自浏览器的HTTP请求
data=connfd.recv(1024*10)
print(data.decode())
#将数据组织为响应格式
response="""HTTP/1.1 200 OK
Content-Type:text/html

This is a test!
"""
# with open("学习机桌面.png","rb") as f:
#     data=f.read()
# response="HTTP/1.1 200 OK\r\n"
# response+="Content-Type:image/jpeg\r\n"
# response+="\r\n"
# response=response.encode()+data



#向浏览器发送内容
connfd.send(response.encode())
connfd.close()
sock.close()