# -*- coding: utf-8 -*-
"""

Function: TF-IDF算法

"""

class TFIDF():
    def __init__(self, ):
        self.tf_dict = {}
        self.idf_dict = {}
        self.words_list = []
        self.tfidf = {}

    def __tran2wordlist(self, sentence_words_list):
        words_list = []
        if len(sentence_words_list) == 0:
            return words_list
        for sentence_list in sentence_words_list:
            if len(sentence_list) == 0:
                continue
            words_list.extend(sentence_list)
        return words_list

    def get_tf(self):
        #注意考虑为0 的情况，拉普拉斯平滑
        sum = len(self.words_list)
        words_dict = {}
        for word in self.words_list:
            words_dict.setdefault(word, 0)
            words_dict[word] += 1
        for key, value in words_dict.items():
            self.tf_dict.setdefault(key, 1.00 * value / sum)

    def get_idf(self, sentence_words_list):
        from math import log
        sentence_length = len(sentence_words_list)
        words_req_dict = {}
        for word in self.words_list:
            words_req_dict.setdefault(word, 0)
            for sentence_list in sentence_words_list:
                if word not in sentence_list:
                    continue
                words_req_dict[word] += 1
        for key, value in words_req_dict.items():
            self.idf_dict.setdefault(key, abs(log(1.0 * sentence_length / value)))

    def get_tfidf(self, sentence_words_list):
        self.words_list = self.__tran2wordlist(sentence_words_list)
        self.get_tf()
        self.get_idf(sentence_words_list)
        for word in self.words_list:
            tf = self.tf_dict.get(word, 0)
            idf = self.idf_dict.get(word, 0)
            self.tfidf.setdefault(word, tf * idf)
        return self.tfidf
