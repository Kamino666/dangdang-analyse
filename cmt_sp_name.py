import pyhanlp
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
import re

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# file_name = "28989328.xlsx"
# data = pd.read_excel(file_name)
data = pd.concat([
    pd.read_excel("22765017.xlsx"),
    pd.read_excel("28973100.xlsx"),
    pd.read_excel("28989328.xlsx"),
    pd.read_excel("29206655.xlsx"),
])
# 使用HanLP提供的Python接口，开启一系列识别
# 包括名字、日本名、音译名、组织名、地区名
segment = pyhanlp.HanLP.newSegment()
segment.enableNameRecognize(True)
segment.enableTranslatedNameRecognize(True)
segment.enableJapaneseNameRecognize(True)
segment.enableOrganizationRecognize(True)
segment.enablePlaceRecognize(True)
# 选出来的一些标注
tokens = [r'/nnt', r'/nnd', r'/nr', r'/nr1', r'/nr1', r'/nrf', r'/nrj',
          r'/ns', r'/nsf', r'/nt', r'/ntc', '/nts', '/ntu', '/nz',
          r'/ntch', '/ntcf', '/ntcb']
detect_words = {i: [] for i in tokens}
detect_words['书名'] = []
for cmt in tqdm(data['comment']):
    # 除了以上，额外获取评论中提到的书籍名称
    book_name = re.findall("《(.*?)》", str(cmt))
    if book_name is not None:
        detect_words['书名'] += book_name
    for w in segment.seg(str(cmt)):
        for t in tokens:
            if t[1:] == str(w).split("/")[1]:
                detect_words[t].append(str(w))
