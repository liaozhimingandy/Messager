from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ReconnectingClientFactory


class ClientProtocol(Protocol):
    def connectionMade(self):
        super().connectionMade()
        self.transport.write("hello".encode('utf-8'))

    def dataReceived(self, data: bytes):
        print(f"{data.decode('utf-8')}")
        # self.transport.write("ok".encode("utf-8"))
        # reactor.stop()


class TestClientFactory(ReconnectingClientFactory):
    """
    todo: 客户端完成自动重试功能
    """

    def __init__(self, maxRetries=3) -> None:
        self.hosts = []
        self.maxRetries = maxRetries
        self.resetDelay()

    protocol = ClientProtocol

    def clientConnectionLost(self, connector, unused_reason):
        print('连接关闭,原因:', unused_reason)
        self.resetDelay()
        super().clientConnectionLost(connector, unused_reason)

    def clientConnectionFailed(self, connector, reason):
        print('Connection failed. Reason:', reason)
        # 更换备用服务器
        # connector.host, connector.port = to_try
        ReconnectingClientFactory.clientConnectionFailed(self, connector,
                                                         reason)


if __name__ == '__main__':

    factory = TestClientFactory()
    reactor.connectTCP('127.0.0.1', 52053, factory)
    reactor.run()
