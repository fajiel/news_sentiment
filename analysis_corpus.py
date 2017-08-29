# -*- coding: utf-8 -*-
"""

Function: 
    1.对语句进行分词；
    2.优化分词结果

"""

import os
import jieba
import yaml
import jieba.analyse
from colorama import Fore
from util import filter_word, NEED_TAGS

TEST_FILE = os.path.abspath("Corpus/test_news")

CUT_WORD_FILE = os.path.abspath("Corpus/sentiment/CUT_WORD.yaml")

class AnalysisCorpus(object):
    def __init__(self):
        self.__load_dict()

    def __load_dict(self):
        """
        Function: 加载yaml文件，获取jieba分词词库配置的词集

        :return: 分句的依赖字典，list形式
        """
        f = open(CUT_WORD_FILE)
        word_dict = yaml.load(f)
        for del_words in word_dict.get("del_word", []):
            jieba.del_word(del_words)
        for add_words in word_dict.get("add_word", []):
            jieba.add_word(add_words)


    def cut_sentence(self, sentence):
        """
        Function: 对句子进行分词
        
        :return: 分词后的list
        """
        # g_sentence为generator类型
        g_sentence = jieba.lcut(sentence, cut_all=False)
        c_sentence = filter(lambda x: filter_word(x), g_sentence)
        return c_sentence

    def cut_content(self, content):
        """
        Function: 对新闻内容进行分句

        :return: 分句后的list
        """
        content_filter = content.replace(" ", "").replace("　", "").replace("\n", "").replace("\t", "")
        content_filter = content_filter.replace("！", "。").replace("？", "。").replace("~", "。").replace("…", "。")
        content_list = content_filter.split("。") #分句方法待优化

        return content_list

    def cut_content_sentence(self, content_list):
        """
        Function: 对新闻内容进行分句

        :return: 分句后的list
        """
        result_list = []
        seg_list = []
        tags_list = []
        for sentence in content_list:
            sentence = sentence.strip()
            sen_list = self.cut_sentence(sentence)
            if not sen_list:
                # print Fore.RED + sentence + u":这是一条无效语句，已被删除!" + Fore.RESET
                continue
            seg = jieba.posseg.cut(sentence)
            tags = jieba.analyse.extract_tags(sentence, topK=1)
            result_list.append(sen_list)
            seg_list.append(seg)
            tags_list.append(tags)
        return result_list, seg_list, tags_list

    def get_depend(self, seg_list, tags_list):
        """
        Function: 获取句法依赖

        :return: 分句的依赖字典，list形式
        """
        NUM = 5
        depend_list = []
        for seg in seg_list:
            tags = tags_list[seg_list.index(seg)]
            seg_dict = {}
            tags_dict = {}
            i = 1
            for word_tuple in seg:
                word = word_tuple.word
                if not filter_word(word):
                    continue
                flag = word_tuple.flag
                if word in tags:
                    tags_dict.setdefault(word, []).append(i)
                seg_dict.setdefault(i, {})
                seg_dict[i].setdefault('word', word)
                seg_dict[i].setdefault('flag', flag)
                i += 1
            depend_dict = {}
            for key, value in tags_dict.items():
                for word_index in value:
                    for i in range(word_index - NUM, word_index + NUM):
                        if not seg_dict.has_key(i):
                            continue
                        depend_dict.setdefault(key, {})
                        depend_dict[key].setdefault(seg_dict[i]['flag'], []).append(seg_dict[i]['word'])

            depend_list.append(depend_dict)

        return depend_list