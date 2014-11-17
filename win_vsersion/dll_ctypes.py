__author__ = 'wanghuafeng'
#coding:utf-8
from ctypes import *
import os
PATH = os.path.dirname(os.path.abspath(__file__))
class HashTable(object):
    '''blizzard hashtable'''
    def __init__(self, hashtable_lenght=2**24):#hashtable_lengh always means the total count of words in your vocabulary, 2**24==16777216 as default!
        self.dll_path = os.path.join(PATH, 'data', 'blizzard_dll.dll')
        self.dll = cdll.LoadLibrary(self.dll_path)
        self.initialize_hashtable(hashtable_lenght)
    def initialize_hashtable(self, hashtable_lenght):
        '''initialize hash table'''
        assert hashtable_lenght&(hashtable_lenght-1)==0
        point = ""
        hashtable_init = self.dll.MPQHashTableInit
        hashtable_init.argtypes = [c_char_p, c_long]
        hashtable_init.restype = c_int
        self.pos_of_hashtable = hashtable_init(point, hashtable_lenght)

    def add(self, val):
        '''add value to hash table'''
        add = self.dll.MPQHashTableAdd
        add.argtypes = [c_char_p, c_int]
        add.restype = c_int
        add_sucess = add(val, self.pos_of_hashtable)
        if add_sucess == 0:#add option failed, means that hashtable_lengh is not long enough...
            raise ValueError('hash table not long enough, please larger your hashtable_lengh param...')

    def check_exists(self, val):
        '''check if val in hash table'''
        check_exist = self.dll.MPQHashTableIsExist
        check_exist.argtypes = [c_char_p, c_int]
        check_exist.restype = c_int
        IsExists = check_exist(val, self.pos_of_hashtable)
        return  False if IsExists==-1 else True

if __name__ == "__main__":
    def test():
        hashtable = HashTable()
        hashtable.add('t1')
        hashtable.add('t2')
        isexists = hashtable.check_exists('t1')
        print isexists
    test()

