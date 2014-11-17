__author__ = 'wanghuafeng'
#coding:utf-8
import os
import sys
import codecs
from collections import deque

try:
    PATH = os.path.dirname(os.path.abspath(__file__))
except:
    PATH = os.getcwd()

class SlicerBase(object):
    def __init__(self, options=None):
        if not options:
            options = {}
        self.options = options
        if not self.options.has_key('vocab_file') or not self.options['vocab_file']:
            self.options['vocab_file'] = os.path.join(PATH, 'data', 'Cizu_and_singleword_komoxo95K.txt')
        self.total_base_word_set = self._load_base_wordlist()

    def _load_base_wordlist(self):
        with codecs.open(self.options['vocab_file'], encoding='utf-8') as f:
            total_base_word_set = set([item.split('\t')[0] for item in f.readlines()])
        return total_base_word_set

    def to_unicode(self, sentence):
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

    def cut_forward(self, complexWords):
        '''cut forword'''
        MAX_LEN = 8
        complexWords = self.to_unicode(complexWords)
        complex_words_lenght = len(complexWords)
        new_postion = 0
        point_position = MAX_LEN
        temp_splited_sentence_list = []
        while point_position-new_postion >= 1:
            point_complex_words = complexWords[new_postion:point_position]
            if point_complex_words in self.total_base_word_set:
                temp_splited_sentence_list.append(point_complex_words)
                new_postion = point_position
                if point_position + MAX_LEN <= complex_words_lenght:
                    point_position = new_postion + MAX_LEN
                else:
                    point_position = complex_words_lenght
                continue
            if new_postion <= complex_words_lenght and point_position == new_postion + 1:
                temp_splited_sentence_list.append(point_complex_words)
                new_postion += 1
                if point_position + MAX_LEN <= complex_words_lenght:
                    point_position = new_postion + MAX_LEN
                else:
                    point_position = complex_words_lenght
                continue
            point_position -= 1
        return temp_splited_sentence_list

    def cut_backwords(self, complexWords):
        '''cut backward '''
        MAX_LEN = 8
        complexWords = self.to_unicode(complexWords)
        point_posttion = len(complexWords)
        new_position = point_posttion - MAX_LEN
        splited_setence_list = deque()
        while point_posttion - new_position >= 1:
            point_complex_words = complexWords[new_position:point_posttion]
            if point_complex_words in self.total_base_word_set:
                splited_setence_list.appendleft(point_complex_words)
                point_posttion = new_position
                if point_posttion - MAX_LEN >= 0:
                    new_position = point_posttion - MAX_LEN
                else:
                    new_position = 0
                continue
            if new_position + 1 == point_posttion and point_posttion >= 0:
                splited_setence_list.appendleft(point_complex_words)
                point_posttion -= 1
                if point_posttion - MAX_LEN >= 0:
                    new_position = point_posttion - MAX_LEN
                else:
                    new_position = 0
                continue
            new_position += 1
        return splited_setence_list

    def slice(self, sentence):
        '''
        if lengh not equal:
            chose the shorter one,
        else:
            chose the back_forward sliced one
        '''
        sentence = self.to_unicode(sentence)
        cut_forward_list = self.cut_forward(sentence)
        cut_backward_list = self.cut_backwords(sentence)
        if len(cut_forward_list) != len(cut_backward_list):
            return min(cut_backward_list, cut_forward_list, key=lambda x:len(x))
        else:
            return cut_backward_list
if __name__ == "__main__":
    def test():
        cp = SlicerBase()
        print ' '.join(cp.cut_backwords('对哈希索引表的算法行封装'))
        print ' '.join(cp.cut_forward('对哈希索引表的算法行封装'))
        print ' '.join(cp.slice('对哈希索引表的算法行封装'))
    test()