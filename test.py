#coding:utf-8
import os
import sys
import codecs
import time
import subprocess
from slicer import SlicerBase
slicebase = SlicerBase()

PATH = os.path.dirname(os.path.abspath(__file__))

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
    splied_words_list = slicebase.slice(sentence)
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

def compile_so():
    '''python call shell to compile c file'''
    command = r'gcc blizzard_hash.c -fPIC -shared -o data/blizzard_hash.so'
    os.system(command)

def check_words_in_base_list(words):
    base_words_set = set()
    filename = os.path.join(PATH, 'data', 'combine_words.txt')
    with codecs.open(filename, encoding='utf-8') as f:
        for line in f.readlines():
            base_words_set.add(line.split('\t')[0])
    print  words in base_words_set

if __name__ == '__main__':
    # check_words_in_base_list(u'引表的算法行封装')
    compile_so()
    # sentence = u'对哈希索引表的算法行封装'
    # print test_slicer(sentence)
    # args = [item for item in sys.argv[1:]]
    # if args[0] == 'slicer' and args[1]:
    #     print test_slicer(args[1]).encode('gbk')
