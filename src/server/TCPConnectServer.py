#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import uuid
import time

from twisted.application import service
from twisted.protocols import policies
from twisted.internet.protocol import connectionDone, ServerFactory
from twisted.internet import protocol

# from src.server import message_pb2


class MessageProtocol(protocol.Protocol, policies.TimeoutMixin):

    def connectionMade(self):
        """建立连接后的回调函数"""
        self.setTimeout(self.factory.TIMEOUT)
        self.factory.numConnections += 1
        # 判断最大连接数,如果超过则断开连接
        if self.factory.numConnections >= self.factory.MAX_CONNECTIONS:
            self.connected = 0
            self.transport.write("Too many connections, try again later".encode("utf-8"))
            self.transport.loseConnection()
            return

        print(f"ip:{self.transport.getPeer().host},port:{self.transport.getPeer().port}......已建立连接;"
              f"目前共{self.factory.numConnections}个连接...")
        self.transport.write("hello".encode("utf8"))
        # ProtobufData(self.transport)

    def dataReceived(self, data):
        """
        接收到客户端的数据
        :param data:
        :return:
        """
        self.resetTimeout()  # 重置超时
        self.transport.write("ok".encode("utf-8"))
        # 解包
        # 根据不同的指令,完成不同的任务
        handle_command()

    def connectionLost(self, reason=connectionDone):  # 在连接关闭时调用
        self.factory.numConnections -= 1
        self.setTimeout(None)
        if self.connected:
            print(f"ip:{self.transport.getPeer().host},port:{self.transport.getPeer().port}......已断开连接;"
                  f"目前共{self.factory.numConnections}个连接...")


class MessageFactory(ServerFactory):
    numConnections = 0
    MAX_CONNECTIONS = 2
    TIMEOUT = 120

    # 指定协议
    protocol = MessageProtocol

    def __init__(self, service):
        self.service = service


class MessageService(service.Service):

    def startService(self):
        print(f"完成初始化")
        service.Service.startService(self)

    def stopService(self):
        super().stopService()
        print(f"服务停止")


def handle_command():
    pass


# def ProtobufData(transport):
#     # 为 IMMessage 填充数据
#     message = message_pb2.IMMessage()
#     message.token = "test"
#     message.msg_type = 30001
#     message.msg_id = str(uuid.uuid4())
#     message.version = "1.0"
#     message._from = "2.0"
#     message._to = "2.0"
#     message.timestamp = int(round(time.time() * 1000000))
#     message.platform = "ANDRIOD"
#     message.message.TextMessage.text = "hello"
#
#     data = message.SerializeToString()
#     transport.write(data)




