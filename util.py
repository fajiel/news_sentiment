# -*- coding: utf-8 -*-


from pyExcelerator import *
from datetime import datetime
from sqlalchemy import Column, String, Integer, Text, create_engine, TIMESTAMP
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine('mysql+mysqlconnector://acount:pwd@IP:PORT/Sentiment?charset=utf8', echo=False)
Session = sessionmaker(bind=engine)  # 创建会话

class News(Base):
    """定义新闻类"""
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True)
    url = Column(String(500), doc=u"主页url")
    source = Column(String(1000), doc=u"来源网站")
    title = Column(String(1000), doc=u"新闻标题")
    # column = Column(String(510), doc=u"专栏")
    author = Column(String(255), doc=u"作者")
    content = Column(Text, doc=u"正文")
    forward = Column(Integer, doc=u"转发量")
    read = Column(Integer, doc=u"阅读量")
    comment = Column(Integer, doc=u"评论量")
    pub_time = Column(TIMESTAMP)
    create_time = Column(TIMESTAMP, nullable=False, default=str(datetime.now()))
    update_time = Column(TIMESTAMP, nullable=False, onupdate=str(datetime.now()))

IGNORE_PUNCT = set(u''':!),.:;?]}¢'"、。〉》」』】〕〗〞︰︱︳﹐､﹒
﹔﹕﹖﹗﹚﹜﹞！），．：；？｜｝︴︶︸︺︼︾﹀﹂﹄﹏､～￠
々‖•·ˇˉ―--′’”([{£¥'"‵〈《「『【〔〖（［｛￡￥〝︵︷︹︻
︽︿﹁﹃﹙﹛﹝（｛“‘-—_…''')


# 去除中文标点符号
def filter_word(word):
    if word in IGNORE_PUNCT:
        return None
    if word in [u'的', u'了', u'和']:
        return None
    if word < u'\u4e00' or word > u'\u9fff':
        return None
    return word

SEN_DICT = {
    "neg": -1,
    "pos": 1,
    "first": 1.0,
    "second": 0.75,
    "third": 0.5,
    "fourth": 0.25,
    "fifth": -0.25,
    "sixth": -0.5,
}

#http://blog.csdn.net/suibianshen2012/article/details/53487157
NEED_TAGS = ['a', 'ad', 'an',
             'b',
             'dg', 'd', 'df',
             'e',
             'f',
             'g',
             'h',
             'i',
             'j',
             'k',
             'l',
             'o',
             'r', 'rr',
             'u', 'uz', 'uv', 'ud', 'ug',
             'v', 'vg', 'vd', 'vn',
             'y',
             'z', 'zg',
             'un',
             ]

def write_excel(input_list):
    book = Workbook()
    sheet1 = book.add_sheet('word')
    sheet1.write(0, 0, u'词性')
    sheet1.write(0, 1, u'词')
    sheet1.write(0, 2, u'积极')
    sheet1.write(0, 3, u'中性')
    sheet1.write(0, 4, u'消极')
    i = 1
    for key, value in input_list:
        sheet1.write(i, 0, key)
        sheet1.write(i, 1, value)
        i += 1
    book.save('need2tag.xls')
