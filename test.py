#coding:utf-8
import os
import sys
#coding:utf-8
import requests
from twisted.internet import protocol, reactor

PATH = os.path.dirname(os.path.abspath(__file__))

def test_http_server():
    '''post and get method'''
    host = 'http://192.168.0.254:5000'
    # host = 'http://127.0.0.1:5000/'
    #***************get_method**************
    html = requests.get('%s?text=%s'%(host, 'helloworld'))
    print html.text
    #***********post_method***************
    post_data = {u'text':u'helloworld'}
    html = requests.post(host, data=post_data)
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

def test_slicer_speed():
    import codecs
    import time
    from slicer import SlicerBase
    slicer = SlicerBase()
    filename = r'F:\CRF\data\tmp_slicer_1.3M_original_data.txt'
    line_list = []
    with codecs.open(filename, encoding='utf-8') as f:
        for sentence in f.readlines():
            splited_sentence = slicer.slice(sentence)
            print ' '.join(splited_sentence)
            time.sleep(1)
            line_list.append(' '.join(splited_sentence)+'\n')
    tmp_file = r'F:\CRF\data\splited_sentence_.txt'
    codecs.open(tmp_file, mode='wb', encoding='utf-8').writelines(line_list)
        # time_interval = time.time() - start_time
        # print time_interval
        # print 74375.0/time_interval
if __name__ == '__main__':
    # test_http_server()
    test_slicer_speed()