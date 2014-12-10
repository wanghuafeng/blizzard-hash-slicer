#coding:utf-8
import codecs
import time
import os
import  codecs

PATH = os.path.dirname(__file__)
def filter_con():
    # filename = r'C:\Users\wanghuafeng\Desktop\dir\nlpcn360w.txt'
    filename= r'F:\CRF\sliced_words_list_360w.txt'
    words_list = []
    with codecs.open(filename, encoding='utf-8') as f:
        for line in f.readlines():
            splited_line = line.split('\t')
            words = splited_line[0]
            p = splited_line[1]
            # if p == 'nw':
            if words[-1] in u'里有的上们会出中以' or words[0] in u'来叫':
                if p == 'nw':
                    continue
            else:
                words_list.append(line)

            # if words[-1] in [u'地', u'着', u'把'] or words[0] == u'在':
            #     if p not in ['nw', 'nrf', 'nr', 'c', 's', 'nrf']:
            #         continue
            # else:
            #     words_list.append(line)

            # if words[0] in [u'的', u'是', u'得', u'和', u'与'] or words[-1] in [u'都', u'到', u'中', u'第', u'和']:
            #     if p not in ['nw', 'nt', 'r', 'nr', 'nrf']:
            #         continue
            # else:
            #     words_list.append(line)

            # if p == 'comb':
            #     if len(words) <= 2 or words[0] in [u'的', u'和'] or words[-1] == u'的':
            #         continue
            # else:
            #     words_list.append(line)
    print len(words_list)
    new_filename = os.path.join(r'F:\CRF', 'words_sliced.txt')
    codecs.open(new_filename, mode='wb', encoding='utf-8').writelines(words_list)
def test_words_in_file(words):
    filename = os.path.join(PATH, 'combine_words.txt')
    total_words_set = set()
    with codecs.open(filename, encoding='utf-8') as f:
        for line in f.readlines():
            total_words_set.add(line.split('\t')[0])
    if words in total_words_set:
        print 'yes'
    else:
        print 'not in file'
words = u'海豚'
test_words_in_file(words)
