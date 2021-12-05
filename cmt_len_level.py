import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
data = pd.concat([
    pd.read_excel("22765017.xlsx"),
    pd.read_excel("28973100.xlsx"),
    pd.read_excel("28989328.xlsx"),
    pd.read_excel("29206655.xlsx"),
])
# 获取数据
data['cmt_length'] = [len(str(i)) for i in data['comment']]
level_length, pic_num = [], []
for level in data['level'].unique():
    level_length.append(data[data['level'] == level]['cmt_length'].mean())
    pic_num.append(data[data['level'] == level]['pic'].mean())

# 绘图
plt.figure(figsize=(18, 10))
plt.subplot(1, 2, 1)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.title("平均评论长度", fontsize=20)
for a, b in zip(data['level'].unique(), level_length):
    plt.text(a, b + 0.05, f"{round(b, 1)}", ha='center', va='bottom', fontsize=20)
plt.ylim(16.0, 20.0)
plt.bar(data['level'].unique(), level_length, label="平均评论长度")

plt.subplot(1, 2, 2)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.title("平均发图数量", fontsize=20)
for a, b in zip(data['level'].unique(), pic_num):
    plt.text(a, b + 0.001, f"{round(b, 3)}", ha='center', va='bottom', fontsize=20)
plt.ylim(0.13, 0.33)
plt.bar(data['level'].unique(), pic_num, label="平均发图数量")

plt.savefig("./cmt_len_level.jpg")
plt.show()
