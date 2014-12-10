__author__ = 'wanghuafeng'
#coding:utf-8
from ctypes import *
import os
PATH = os.path.dirname(os.path.abspath(__file__))

class HashTable(object):
    '''blizzard hashtable'''
    def __init__(self, hashtable_lenght=2**22):
        self.dll_path = os.path.join(PATH, 'data', 'blizarrd_hashA_hashB.dll')# platfor of winodows
        # self.dll_path = os.path.join(PATH, 'data', 'blizzard_hash.so')# platfor of linux
        # self.dll_path = os.path.join(r'F:\c_project\blizarrd_hashA_hashB\x64\Debug', 'blizarrd_hashA_hashB.dll')
        # self.dll_path = os.path.join(r'F:\c_project\blizza_crash\x64\Debug', 'blizza_crash.dll')
        self.dll = cdll.LoadLibrary(self.dll_path)
        self.initialize_hashtable(hashtable_lenght)
        self._initialize_add_param()
        self._initialize_checkExists_param()

    def initialize_hashtable(self, hashtable_lenght):
        '''initialize hash table'''
        assert hashtable_lenght&(hashtable_lenght-1)==0
        point = ""
        hashtable_init = self.dll.MPQHashTableInit
        hashtable_init.argtypes = [c_char_p, c_long]
        hashtable_init.restype = c_void_p
        self.pos_of_hashtable = hashtable_init(point, hashtable_lenght)
        # print self.pos_of_hashtable

    def _initialize_add_param(self):
        '''initialize add param by ctypes'''
        self.fun_add = self.dll.MPQHashTableAdd
        self.fun_add.argtypes = [c_char_p, c_void_p]
        self.fun_add.restype = c_uint

    def _initialize_checkExists_param(self):
        '''initialize checkExists param by ctypes'''
        self.fun_check_exist = self.dll.MPQHashTableIsExist
        self.fun_check_exist.argtypes = [c_char_p, c_void_p]
        self.fun_check_exist.restype = c_long

    def add(self, val):
        '''add value to hash table'''
        add_sucess = self.fun_add(val, self.pos_of_hashtable)
        if add_sucess == 0:
            raise ValueError('hash table not long enough, please enlarge your hashtable_lengh param...')

    def check_exists(self, val):
        '''check if val in hash table'''
        IsExists = self.fun_check_exist(val, self.pos_of_hashtable)
        return IsExists

if __name__ == "__main__":
    def test():
        hashtable = HashTable()
        # print 'before add'
        hashtable.add('哈希')
        # print 't1 added sucessed'
        # print 't2 before add...'
        hashtable.add('引表')
        # print 't2 end add...'
        isexists = hashtable.check_exists('引表')
        if isexists:
            print 'yes'
        else:
            print 'not in hash'
    test()


