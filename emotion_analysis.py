'''
    评论内容情感分析以及词云生成
'''

import numpy as np
import pymysql
from snownlp import SnowNLP
from pyecharts.charts import Bar
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import jieba
from musics import sql


def getComments():
    comments = sql.get_comments()
    return comments

def getSemi(text):
    text['COMMENTS'] = text['COMMENTS'].apply(lambda x:round(SnowNLP(x).sentiments, 2))
    semiscore = text.groupby(text['COMMENTS']).count()
    bar = Bar('评论情感得分')
    bar.use_theme('dark')
    bar.add('', y_axis = semiscore.values, x_axis = semiscore.index.values, is_fill=True,)
    bar.render(r'情感得分分析.html')

    text['COMMENTS'] = text['COMMENTS'].apply(lambda x:1 if x>0.5 else -1)
    semilabel = text.groupby(text['COMMENTS']).count()
    bar = Bar('评论情感标签')
    bar.use_theme('dark')
    bar.add(
        '',
        y_axis = semilabel.values,
        x_axis = semilabel.index.values,
        is_fill=True,
    )
    bar.render(r'情感标签分析.html')

plt.style.use('ggplot')
plt.rcParams['axes.unicode_minus'] = False

def getWordcloud(comments):
    text = ''.join(s['COMMENTS'] for s in comments if s)
    word_list = jieba.cut(text, cut_all = False)
    print(word_list)
    stopwords = [line.strip() for line in open(r'./StopWords.txt', 'r').readlines()]  # 导入停用词
    clean_list = [seg for seg in word_list if seg not in stopwords]  # 去除停用词
    clean_text = ''.join(clean_list)
    # 生成词云
    cloud = WordCloud(
		scale = 4,
        font_path=r'C:/Windows/Fonts/msyh.ttc',
        background_color='white',
        max_words = 2000,
        max_font_size = 64
    )
    word_cloud = cloud.generate(clean_text)
    # 绘制词云
    plt.figure(figsize=(10, 10))
    plt.imshow(word_cloud)
    plt.axis('off')
    plt.show()

if __name__ == '__main__':
    comments = getComments()
    getWordcloud(comments)
    text = sql.get_text()
    getSemi(text)
