#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import uuid
import time

from twisted.protocols import policies
from twisted.internet.protocol import Factory, connectionDone
from twisted.internet import reactor, protocol

import message_pb2


class MessageProtocol(protocol.Protocol, policies.TimeoutMixin):
    def __init__(self, factory):
        self.factory = factory
        self.setTimeout(self.factory.timeout)
        self.connected = 1
        self.factory.numConnections += 1

    def connectionMade(self):  # 建立连接后的回调函数
        # 判断最大连接数,如果超过则断开连接
        if(self.factory.numConnections >= self.factory.MAX_CONNECTIONS): 
            self.connected = 0
            self.transport.write('Too many connections, try again later')
            self.transport.loseConnection()
            return

        print(f"ip:{self.transport.getPeer().host},port:{self.transport.getPeer().port}......已建立连接;目前共{self.factory.numConnections}个连接...")
        # self.transport.write("hello".encode("utf8"))
        ProtobufData(self.transport)
        

    def dataReceived(self, data): 
        '''
        接收到客户端的数据
        :param data:
        :return:
        '''
        self.resetTimeout() # 重置超时
        self.transport.write("ok".encode("utf-8"))
        # 解包
        # 根据不同的指令,完成不同的任务
        handle_command()

    def connectionLost(self, reason=connectionDone):  # 在连接关闭时调用
        self.factory.numConnections -= 1
        self.setTimeout(None)
        if(self.connected):
            print(f"ip:{self.transport.getPeer().host},port:{self.transport.getPeer().port}......已断开连接;目前共{self.factory.numConnections}个连接...")


class MessageFactory(Factory):
    numConnections = 0
    MAX_CONNECTIONS = 2
    def __init__(self, quote=None, timeout=120): 
        self.timeout = timeout

    def buildProtocol(self, addr):
        return MessageProtocol(self)


def handle_command():
    pass


def ProtobufData(transport):
    # 为 IMMessage 填充数据
    message = message_pb2.IMMessage()
    message.token = "test"
    message.msg_type = 30001
    message.msg_id = str(uuid.uuid4())
    message.version = "1.0"
    message._from = "2.0"
    message._to = "2.0"
    message.timestamp = int(round(time.time() * 1000000))
    message.platform = "ANDRIOD"
    message.message.TextMessage.text = "hello"

    data = message.SerializeToString()
    transport.write(data)


if __name__ == '__main__':
    SERVER_PORT = 52053 # 监听的端口
    TIMEOUT = 120 # 超时时间
    host = "localhost"
    from optparse import OptionParser
    #设置server启动选项
    parser = OptionParser()
    parser.add_option("--host", default=host,
        dest="host", help="host address [default: %default]")
    parser.add_option("-p", "--port", default=SERVER_PORT,
        dest="port", help="Application port number [default: %default]")
    (opt, args) = parser.parse_args()
    print(f"Running Socket AMF gateway on {opt.port}")
    reactor.listenTCP(int(opt.port), MessageFactory(timeout=TIMEOUT))
    print(f"{'*'*8}正在监听本地端口:{int(opt.port)}{'*'*8}")
    reactor.run()