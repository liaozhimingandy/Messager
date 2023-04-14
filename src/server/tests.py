from twisted.trial._asynctest import TestCase


class PoetryTestCase(TestCase):

    def setUp(self):
        pass
        # from twisted.internet import reactor
        # self.port = reactor.listenTCP(0, factory, interface="127.0.0.1")
        # self.portnum = self.port.getHost().port