import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def plot_figure(file_name, color='b', label=''):
    data = pd.read_excel(file_name)
    data['time'] = pd.to_datetime(data['time'])
    data = data.set_index('time')
    data['cmt_count'] = 1
    data_week = data[1:].resample("SM").sum()
    plt.plot(data_week.index, data_week['cmt_count'], color=color, label=label)


def func2():
    plt.figure(figsize=(20, 10))
    plot_figure("22765017.xlsx", 'b', '22765017')
    plot_figure("28973100.xlsx", 'r', '28973100')
    plot_figure("28989328.xlsx", 'black', '28989328')
    plot_figure("29206655.xlsx", 'g', '29206655')
    plt.xticks(rotation=30, fontsize=20)
    plt.legend(fontsize=20)
    ax = plt.gca()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(90))

    plt.savefig("cmt_number2.jpg")
    plt.show()

func2()