# -*- coding: utf-8 -*-
"""

Function: 计算新闻类文本的情感分析

"""

from analysis_corpus import AnalysisCorpus
from ifidf import TFIDF
from extract_sentences import ExtractThemeSentences
from calc_sentiment import ClacSentiment

def gen_themeset(tfidf_dict, title_list):
    #获取完整主题集
    if not tfidf_dict:
        return {}
    theme_set = {}
    theme_set.update(tfidf_dict)
    tfidf_list= theme_set.values()
    max_tfidf = max(tfidf_list)
    min_tfidf = min(tfidf_list)
    #title的权重较高，做特殊处理
    max_threshold = min_tfidf + 0.85 * (max_tfidf - min_tfidf)
    min_threshold = min_tfidf + 0.55 * (max_tfidf - min_tfidf)
    for title_word in title_list:
        if theme_set.has_key(title_word) and theme_set[title_word] < max_threshold:
            theme_set[title_word] = max_threshold
        elif not theme_set.has_key(title_word):
            theme_set[title_word] = min_threshold
    return theme_set

def gen_sen_tfidf(theme_set, sentence_words_list):
    sen_tfidf_list = []
    for sentence_list in sentence_words_list:
        sen_tfidf_list.append([theme_set[word] for word in sentence_list])
    return sen_tfidf_list

def sen_title_count(title_list, sentence_words_list):
    sen_title_list = []
    for sentence_list in sentence_words_list:
        word_count = 0
        for word in title_list:
            word_count += sentence_list.count(word)
        sen_title_list.append(word_count)
    return sen_title_list

def vector_proc(theme_set, sentence_words_list):
    words_list = theme_set.keys()
    theme_list = [theme_set[word] for word in words_list]
    sen_list = []
    for sentence_list in sentence_words_list:
        temp_list = []
        for word in words_list:
            count = sentence_list.count(word)
            simi = theme_set.get(word, 0)
            temp_list.append(1.00 * count * simi)
        sen_list.append(temp_list)
    return theme_list, sen_list

def get_sentiment(sen_score_list, sentiment_list):
    sort_score_list = sorted(sen_score_list, reverse=True)

    if len(sen_score_list) in range(3,11):
        length = 3
    elif len(sen_score_list) > 10:
        length = 30 * len(sen_score_list) / 100
    else:
        length = len(sen_score_list)

    theme_score_list = sort_score_list[:length+1]
    sentiment = 0.00
    for sen_score in theme_score_list:
        sen_index = sen_score_list.index(sen_score)
        value = sentiment_list[sen_index]
        sentiment += value
    return sentiment / len(theme_score_list)

def clac_sentiment(title, content):
    ac = AnalysisCorpus()
    # 获取新闻名称的分词列表。
    title_list = ac.cut_sentence(title)
    # 获取新闻内容的分句列表。
    content_list = ac.cut_content(content)
    if len(content_list) == 0:
        return 0
    # 获取新闻内容的分词列表。格式：[[],[],[],]
    sentence_words_list, seg_list, tags_list = ac.cut_content_sentence(content_list)

    # 获取句法依存提取
    depend_list = ac.get_depend(seg_list, tags_list)

    tfidf_obj = TFIDF()
    tfidf_dict = tfidf_obj.get_tfidf(sentence_words_list)

    # 获取完整主题集
    theme_set = gen_themeset(tfidf_dict, title_list)
    theme_list, sen_list = vector_proc(theme_set, sentence_words_list)
    sen_tfidf_list = gen_sen_tfidf(theme_set, sentence_words_list)
    sen_title_list = sen_title_count(title_list, sentence_words_list)
    # 提取主题句
    them_obj = ExtractThemeSentences()
    sen_score_list = them_obj.get_score(theme_list, sen_list, sen_tfidf_list, sen_title_list)

    score_cut_list = []
    for i in range(len(sen_score_list)):
        score_cut_list.append([sen_score_list[i], "|".join(sentence_words_list[i])])

    if len(sen_score_list) == 0:
        return 0
    cs = ClacSentiment()
    sentiment_list, words = cs.get_sen(depend_list)
    sentiment = get_sentiment(sen_score_list, sentiment_list)
    return sentiment, words

def main():
    title = "习近平对河北塞罕坝林场建设者感人事迹作出重要指示"
    content = "新华社北京8月28日电 中共中央总书记、国家主席、中央军委主席习近平近日对河北塞罕坝林场建设者感人事迹作出重要指示指出，55年来，河北塞罕坝林场的建设者们听从党的召唤，在“黄沙遮天日，飞鸟无栖树”的荒漠沙地上艰苦奋斗、甘于奉献，创造了荒原变林海的人间奇迹，用实际行动诠释了绿水青山就是金山银山的理念，铸就了牢记使命、艰苦创业、绿色发展的塞罕坝精神。他们的事迹感人至深，是推进生态文明建设的一个生动范例。"
    sentiment, words = clac_sentiment(title, content)

    print(sentiment, "|".join(words))

if __name__ == "__main__":
    main()