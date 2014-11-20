#encoding:utf-8
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import Factory
from twisted.internet import reactor
import struct
from slicer import SlicerBase
# slicebase = SlicerBase()

def to_unicode(sentence):
    sentence = sentence.strip()
    if isinstance(sentence, str):
        try:
            sentence = sentence.decode('utf-8')
        except Exception,e:
            sentence = sentence.decode('gbk', 'ignore')
    return sentence

def to_utf8(sentence):
    sentence = sentence.strip()
    if isinstance(sentence, str):
        try:
            sentence = sentence.decode('ascii')
        except Exception, e:
            sentence = sentence.decode('gbk', 'ignore')
    sentence = sentence.encode('utf-8')
    return sentence

class SlicerProtocol(Protocol):
    def __init__(self, slicer):
        self.slicer = slicer

    def dataReceived(self, data):
        sentence = data.decode('utf-8').encode('utf-8')
        splited_words_list = self.slicer.slice(sentence)
        # print splited_words_list
        self.transport.write(' '.join(splited_words_list).encode('utf-8'))

class SlicerFactory(Factory):
    def buildProtocol(self, addr):
        slicebase = SlicerBase()
        return SlicerProtocol(slicebase)

reactor.suggestThreadPoolSize(8)

reactor.listenTCP(5001, SlicerFactory())
reactor.run()
