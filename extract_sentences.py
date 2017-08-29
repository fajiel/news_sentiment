# -*- coding: utf-8 -*-
"""
Function: 提取主题句；
    
Desc: 依据以下四项计算文章各句子得分，确立主题句。
    1.计算余弦距离；
    2.计算位置得分；
    3.计算机中长度分值；
    4.计算标题相似度
       
"""
import numpy as np
from numpy import ndarray
from math import sqrt

class ExtractThemeSentences():
    def __init__(self):
        self.cos_score = []
        self.loc_score = []
        self.len_score = []
        self.simi_score = []

    def __scaling(self, score_list):
        if not score_list:
            return []
        result_list = []
        score_dist = max(score_list) - min(score_list)
        for score in score_list:
            result_list.append(1.00 * (score - min(score_list) + 1) / (score_dist + 2))
        return result_list

    def calc_cos(self, theme_list, sen_list):
        """
        Func: 计算两个向量的余弦相似度
        :return: self.cos_score
        """
        theme_vector = np.array(theme_list)
        cos_list = []
        for signal_sen in sen_list:
            sen_vector = np.array(signal_sen)
            sen_tran = sen_vector.transpose()
            # 余弦计算方法
            single_cos = 1.00 * theme_vector.dot(sen_tran) / (sqrt(theme_vector.dot(theme_vector.transpose())) * sqrt(sen_vector.dot(sen_vector.transpose())))
            cos_list.append(single_cos)

        self.cos_score = self.__scaling(cos_list)

    def calc_loc(self, sen_list):
        """
        Func: 计算语句在文章中的位置分值，并做归一化处理
        :return: 
        """
        sen_len = len(sen_list)
        loc_list = []
        for i in range(sen_len):
            single_score = sqrt((i - (sen_len + 1)/2) * (i - (sen_len + 1)/2))
            loc_list.append(single_score)

        self.loc_score = self.__scaling(loc_list)

    def calc_len(self, sen_tfidf_list):
        """
        Func: 计算语句的标题相似度
        :return: 
        """
        len_list = []
        for tfidf_list in sen_tfidf_list:
            len_list.append(sum(tfidf_list) / sqrt(len(tfidf_list)))

        self.len_score = self.__scaling(len_list)

    def calc_simi(self, sen_title_list):
        self.simi_score = self.__scaling(sen_title_list)

    def get_score(self, theme_list, sen_list, sen_tfidf_list, sen_title_list):
        self.calc_cos(theme_list, sen_list)
        self.calc_loc(sen_list)
        self.calc_len(sen_tfidf_list)
        self.calc_simi(sen_title_list)
        cos_array = 0.75 * np.array(self.cos_score)
        loc_array = 0.2 * np.array(self.loc_score)
        len_array = 0.1 * np.array(self.len_score)
        simi_array = 0.15 * np.array(self.simi_score)
        score_list = cos_array + len_array + simi_array# + loc_array

        return ndarray.tolist(score_list)