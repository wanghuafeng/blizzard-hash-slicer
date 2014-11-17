__author__ = 'wanghuafeng'
#coding:utf-8
from ctypes import *
import os
PATH = os.path.dirname(os.path.abspath(__file__))

class HashTable(object):
    '''blizzard hashtable'''
    def __init__(self, hashtable_lenght=2**22):
        self.dll_path = os.path.join(PATH, 'data', 'blizzard_hash.so')
        self.dll = cdll.LoadLibrary(self.dll_path)
        self.initialize_hashtable(hashtable_lenght)

    def initialize_hashtable(self, hashtable_lenght):
        '''initialize hash table'''
        assert hashtable_lenght&(hashtable_lenght-1)==0
        point = ""
        hashtable_init = self.dll.MPQHashTableInit
        hashtable_init.argtypes = [c_char_p, c_long]
        hashtable_init.restype = c_void_p
        self.pos_of_hashtable = hashtable_init(point, hashtable_lenght)
        # print self.pos_of_hashtable

    def add(self, val):
        '''add value to hash table'''
        add = self.dll.MPQHashTableAdd
        add.argtypes = [c_void_p, c_void_p]
        add.restype = c_uint
        add_sucess = add(cast(val, c_char_p), self.pos_of_hashtable)
        if add_sucess == 0:
            raise ValueError('hash table not long enough, please enlarge your hashtable_lengh param...')

    def check_exists(self, val):
        '''check if val in hash table'''
        check_exist = self.dll.MPQHashTableIsExist
        check_exist.argtypes = [c_void_p, c_void_p]
        check_exist.restype = c_long
        IsExists = check_exist(cast(val, c_char_p), self.pos_of_hashtable)
        return IsExists != -1

if __name__ == "__main__":
    def test():
        hashtable = HashTable()
        # print 'before add'
        hashtable.add('哈希')
        # print 't1 added sucessed'
        # print 't2 before add...'
        hashtable.add('引表')
        # print 't2 end add...'
        isexists = hashtable.check_exists('引')
        print isexists
    # test()
    import codecs
    import time
    def test_words_in_file():
        hastable = HashTable()
        filename = os.path.join(os.path.dirname(__file__), 'data', 'combine_words.txt')
        with codecs.open(filename) as f:
            for line in f.readlines():#[:1155]:
                words = line.split('\t')[0]
                hastable.add(words)
        isexists = hastable.check_exists('表引表引表表引表引表')
        print isexists
    test_words_in_file()

