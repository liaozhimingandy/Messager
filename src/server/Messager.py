from twisted.application import service
from twisted.application.internet import TCPServer

import sys
sys.path.append("../..")

from src.server import TCPConnectServer

port = 52053
iface = 'localhost'

top_service = service.MultiService()
message_service = TCPConnectServer.MessageService()
message_service.setServiceParent(top_service)

factory = TCPConnectServer.MessageFactory(message_service)
tcp_service = TCPServer(port, factory, interface=iface)
tcp_service.setServiceParent(top_service)

# this variable has to be named 'application'
application = service.Application("messager")

# this hooks the collection we made to the application
top_service.setServiceParent(application)
