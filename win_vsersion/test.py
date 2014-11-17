#coding:utf-8
import sys
import codecs
import time
from slicer import SlicerBase
slicebase = SlicerBase()

def to_unicode(sentence):
    sentence = sentence.strip()
    if isinstance(sentence, str):
        try:
            sentence = sentence.decode('utf-8')
        except Exception,e:
            try:
                sentence = sentence.decode('gbk')
            except Exception:
                raise ValueError('unknown coding...')
    return sentence

def test_slicer(sentence):
    sentence = to_unicode(sentence)
    splied_words_list = slicebase.cut_backwords(sentence)
    return ' '.join(splied_words_list)

def test_slicer_speed():
    '''测试切词速度'''
    slice = SlicerBase()
    uncuted_filename = 'temp.txt'
    with codecs.open(uncuted_filename, encoding='utf-8') as f:
        sentence_list = [item.strip() for item in f.readlines()]
        start_time = time.time()
        for sentence in sentence_list:
            slice.slice(sentence)
        print time.time()-start_time

if __name__ == '__main__':
    # sentence = u'对哈希索引表的算法行封装'
    # print test_slicer(sentence)
    args = [item for item in sys.argv[1:]]
    if args[0] == 'slicer' and args[1]:
        print test_slicer(args[1]).encode('gbk')
