#coding:utf-8
import os
import sys
#coding:utf-8
import requests
from twisted.internet import protocol, reactor

PATH = os.path.dirname(os.path.abspath(__file__))

def test_http_server():
    '''Usage: http://127.0.0.1:5000/?text=your sentence here'''
    host = 'http://192.168.0.254:5000/'
    locathost = '127.0.0.1:5000'
    html = requests.get('%s?text=%s'%(host, 'helloworld'))
    print html.text

def test_socket_server():
    HOST = '192.168.133.132'
    PORT = 5001
    class TSClntProtocol(protocol.Protocol):
        def sendData(self):
            data = raw_input('> ')
            if data:
                print '...sending %s...'%data
                self.transport.write(data)
            else:
                self.transport.loseConnection()
        def connectionMade(self):
            self.sendData()
        def dataReceived(self, data):
            print data
            self.sendData()

    class TSClntFactory(protocol.ClientFactory):
        protocol = TSClntProtocol
        clientConnectionLost = clientConnectionFailed = lambda self, connector, reason:reactor.stop()

    reactor.connectTCP(HOST, PORT, TSClntFactory())
    reactor.run()

if __name__ == '__main__':
    test_socket_server()