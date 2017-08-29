# -*- coding: utf-8 -*-
"""
Function: 根据句法依存计算各分句情感值；
    
Desc: 
    1.入参：各句子的中心词及其修饰词；
    2.依据情感词典。
       
"""
import os
import yaml
from util import SEN_DICT
WORD_FILE = os.path.abspath("Corpus/sentiment/SEN_WORD_DICT.yaml")
class ClacSentiment():
    def __init__(self):
        self.all_sen_dict = {}

    def __reversal(self, input_dict):
        """
        Function: 字典翻转

        :return: 字典，key为情感词，value为情感值
        """
        output_dict = {}
        for key, value in input_dict.items():
            if not SEN_DICT.has_key(key):
                continue
            result = SEN_DICT[key]
            for word in value:
                output_dict.setdefault(word, result)
        return output_dict

    def gen_sen_dict(self):
        """
        Function: 加载yaml文件，获取情感词典

        :return: 分句的依赖字典，list形式
        """
        f = open(WORD_FILE)
        word_dict = yaml.load(f)
        self.all_sen_dict = self.__reversal(word_dict)

    def get_sen(self, depend_list):
        """
        Function: 获取情感值

        :return: 各句子情感值，list给出
        """
        sen_list = []
        words = []
        self.gen_sen_dict()
        i = 0
        for depend_dict in depend_list:
            temp_value = 1.00
            neu_flag = True
            for theme_word, depend_word in depend_dict.items():
                for word_type, word_list in depend_word.items():
                    words.extend(word_list)
                    word_list = list(set(word_list))
                    for word in word_list:
                        if word in self.all_sen_dict:
                            neu_flag = False
                        temp_value *= self.all_sen_dict.get(word, 1.00)
            if neu_flag:
                temp_value = 0
            sen_list.append(temp_value)
            i += 1
        return sen_list, list(set(words))