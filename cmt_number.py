import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.ticker as ticker

def plot_figure(file_name):
    data = pd.read_excel(file_name)
    data['time'] = pd.to_datetime(data['time'])  # 转换成时间格式
    data = data.set_index('time')  # 设置成index
    data['cmt_count'] = 1
    data_week = data[1:].resample("W").sum()  # 按照周计算评论数量
    data_week = data_week[data_week.index > datetime(2021, 8, 1)]
    plt.bar(data_week.index, data_week['cmt_count'], width=3, align='center')
    plt.xticks(rotation=30)
    ax = plt.gca()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(7))
    plt.title(file_name, fontsize=20)

plt.figure(figsize=(18, 12))
plt.subplot(2, 2, 1)
plot_figure("22765017.xlsx")
plt.subplot(2, 2, 2)
plot_figure("28973100.xlsx")
plt.subplot(2, 2, 3)
plot_figure("28989328.xlsx")
plt.subplot(2, 2, 4)
plot_figure("29206655.xlsx")
# plt.savefig("cmt_number.jpg")
plt.show()
