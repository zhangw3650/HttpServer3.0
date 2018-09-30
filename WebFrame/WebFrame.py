# coding=utf-8
'''
Author:  zhangw
tine : 2018-10-1
'''

from socket import *
from setting import *
from urls import *
from views import *
import time


class Application(object):
    def __init__(self):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.sockfd.bind(frame_addr)

    def start(self):
        self.sockfd.listen(5)
        while True:
            connfd, addr = self.sockfd.accept()
            # 接收请求方法
            method = connfd.recv(128).decode()
            # 接收请求方法
            path = connfd.recv(128).decode()

            if method == 'GET':
                print("请求内容:", path)
                if path == '/' or path[-5:] == '.html':
                    status, response_body = self.get_html(path)
                else:
                    status, response_body = self.get_data(path)

                # 将结果发送给httpserver
                connfd.send(status.encode())
                time.sleep(0.1)
                connfd.send(response_body.encode())
                connfd.close()

            if method == 'POSt':
                pass

    def get_html(self, path):
        if path == '/':
            get_file = STATIC_DIR + '/index.html'
        else:
            get_file = STATIC_DIR + path

        try:
            f = open(get_file)
        except IOError:
            response = ('404', "==Sorry not found the page==")
        else:
            response = ('200', f.read())
        finally:
            return response

    def get_data(self, path):
        for url, handler in urls:
            if path == url:
                response_body = handler()
                return '200', response_body
        return '404', 'Sorry,Not found the data'


if __name__ == "__main__":
    app = Application()
    app.start()  # 启动框架等待request
