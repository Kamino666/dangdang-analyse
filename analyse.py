from jieba import analyse
import wordcloud
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt

# 读取数据
# data = pd.read_excel("22765017.xlsx")
# 读取获取所有的差评
data = pd.concat([
    pd.read_excel("22765017.xlsx"),
    pd.read_excel("28973100.xlsx"),
    pd.read_excel("28989328.xlsx"),
    pd.read_excel("29206655.xlsx"),
])
data = data[data['star'] < 8]

all_comments = data['comment']
# 使用词频计数器
cnt_tags = Counter()
cnt_tr = Counter()
for cmt in all_comments:
    cmt = str(cmt)
    tags = analyse.extract_tags(cmt)  # 基于TF-IDF的算法
    cnt_tags += Counter(tags)
    trs = analyse.textrank(cmt)       # 基于TextRank的算法
    cnt_tr += Counter(trs)

stop_words = ['没有', '这个', '不过', '本书', '真的', '应该', '感觉']
for k in stop_words:
    del cnt_tags[k]
    del cnt_tr[k]
w = wordcloud.WordCloud(
    font_path=r"C:\Users\Kamino\AppData\Local\Microsoft\Windows\Fonts\FZYanSJW_0.TTF",
    width=1600, height=1200, background_color='white', max_words=60,
    stopwords=set(stop_words), colormap=plt.get_cmap("tab20c"),
    max_font_size=400, prefer_horizontal=1.0
)
w.fit_words(dict(cnt_tags))
w.to_file("bad_tags.png")

w = wordcloud.WordCloud(
    font_path=r"C:\Users\Kamino\AppData\Local\Microsoft\Windows\Fonts\FZYanSJW_0.TTF",
    width=1600, height=1200, background_color='white', max_words=60,
    stopwords=set(stop_words), colormap=plt.get_cmap("tab20c"),
    max_font_size=400, prefer_horizontal=1.0
)
w.fit_words(dict(cnt_tr))
w.to_file("bad_textrank.png")

