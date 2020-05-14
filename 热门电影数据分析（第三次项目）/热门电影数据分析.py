import pandas as pd
import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import re


def jieba_fenci(*evaluates):  # 依据参数传递的数据，对评论进行分类并分词
    counts = {}
    for evaluate in evaluates:
        for i in range(len(csv_data)):
            if csv_data.iloc[i][1] == evaluate:
                words = jieba.lcut(csv_data.iloc[i][4])  # 采用全模式进行分词，存在冗余
                for word in words:
                    counts[word] = counts.get(word, 0) + 1
    return counts


def remove_words(data):  # 去除停用词
    # stop_list = []  # 用于保存去除“\n”后的停用词列表
    # stoplist = open("stoplist.txt", 'r', encoding='utf-8').readlines()  # 读取停用词列表
    # for word in stoplist:
    #     stop_list.append(word.strip('\n'))
    stop_list = open("stoplist.txt", 'r', encoding='utf-8').read()
    stop_list = stop_list.split()
    stop_list = [' ', '电影', '流浪', '地球'] + stop_list    # 因为split去除了空格，故需加回，也可在[]中加入其它停用词
    for stop in stop_list:
        if stop in data:  # 判断停用词是否在字典的键中
            del data[stop]
    # if ' ' in data:  # 分词时空白也被认为是一个词，故予以去除
    #     del data[' ']
    return data


def tuple_to_list(ls):  # 将列表中元组所含的键和值分离
    key = []
    values = []
    for item in ls:
        key.append(item[0])
        values.append(item[1])
    return key, values


def words_counts():  # 词频统计并将其保存为csv文件
    list_hao = list(counts_hao.items())  # 将字典转为列表，为对其值进行排序做准备
    list_hao.sort(key=lambda x: x[1], reverse=True)  # lambda用来指定使用哪一个多元选项的列作为排列序，默认的排序方法是从小到大
    list_zhong = list(counts_zhong.items())
    list_zhong.sort(key=lambda x: x[1], reverse=True)
    list_cha = list(counts_cha.items())
    list_cha.sort(key=lambda x: x[1], reverse=True)
    hao, values1 = tuple_to_list(list_hao)
    zhong, values2 = tuple_to_list(list_zhong)
    cha, values3 = tuple_to_list(list_cha)
    dl1 = {'好评分词': hao, '好评词频': values1}
    dl2 = {'中评分词': zhong, '中评词频': values2}
    dl3 = {'差评分词': cha, '差评词频': values3}
    df = pd.concat([pd.DataFrame(dl1), pd.DataFrame(dl2), pd.DataFrame(dl3)], axis=1)
    # 将数据量不同的列表整合为一张表，注意要加axis=1 ，不然数据不会对齐
    df.to_csv('词频统计.csv', encoding='utf-8_sig', index=False)
    print('词频统计已完成，数据已保存在：词频统计.csv文件中！')


def draw_wordcloud():   # 绘制词云
    # pic = plt.imread()    # 可导入背景
    print('绘制词云中，请稍候：')
    wc = WordCloud(background_color='white', font_path='c:\\Windows\\Fonts\\simkai.ttf',
                   width=1920, height=1080)
    wc_hao = wc.fit_words(counts_hao)  # 传入词频
    wc_hao.to_file("好评词云.jpg")
    wc_zhong = wc.fit_words(counts_zhong)
    wc_zhong.to_file('中评词云.jpg')
    wc_cha = wc.fit_words(counts_cha)
    wc_cha.to_file('差评词云.jpg')
    # plt.imshow(wc_hao)
    # plt.axis('off')    # 去除黑色边框
    # plt.show()         # 直接显示
    print('词云绘制完成，已保存为jpg文件！')


def times(start, end):   # 输入时间字符串的索引区间，返回对区间进行分类的字典
    counts = {}
    for i in range(len(csv_data)):
        day = (csv_data.iloc[i][2])[start:end]
        counts[day] = counts.get(day, 0) + 1
    return counts


def scores_everyday():  # 将每天的评分平均化，并保存为字典
    counts = {}
    for i in range(len(csv_data)):                         # 将相同日期的评分提取出来，并构成字典
        key = (csv_data.iloc[i][2])[0:10]
        values = []
        values.append(eval(csv_data.iloc[i][0].replace('allstar', '').replace('rating', '')))
        if key in counts:
            counts[key] += values
        else:
            counts[key] = values
    for k in dict.keys(counts):                  # 将相同日期的评分求平均数
        s = 0
        for num in counts[k]:
            s += num
        counts[k] = s/len(counts[k])
    return counts


def translate(date, start, end):      # 取出日期的年
    ls = []
    for item in date:
        ls.append(item[start:end])
    return ls


def hui_tu():
    list_days = list(days_dict.items())
    list_days.sort(key=lambda x: x[0], reverse=False)
    days, values_days = tuple_to_list(list_days)
    days = translate(days, 5, 10)
    plt.figure(figsize=(16, 9))    # 去除日期中的年
    plt.title('用户发表短评数量随日期的变化情况', fontproperties='SimHei', fontsize=20)
    plt.xlabel("日期", fontproperties='SimHei', fontsize=20)
    plt.ylabel("短评数量", fontproperties='SimHei', fontsize=20)
    plt.plot(days, values_days, '-.')
    plt.grid(True, linestyle = "--", color="gray", linewidth="0.5")     # 加入网格
    # plt.tick_params(labelsize=8)    # 设置xy坐标刻度字体大小
    plt.xticks(fontsize=8)
    plt.savefig('用户发表短评数量随日期的变化情况', dpi=600)
    print("用户发表短评数量随日期的变化情况图表绘制完成，已保存！")

    list_times = list(times_dict.items())
    list_times.sort(key=lambda x: x[0], reverse=False)
    time, values_time = tuple_to_list(list_times)
    plt.figure(figsize=(16, 9))
    plt.title('用户发表短评数量随时刻的变化情况', fontproperties='SimHei', fontsize=20)
    plt.xlabel("时间", fontproperties='SimHei', fontsize=20)
    plt.ylabel("短评数量", fontproperties='SimHei', fontsize=20)
    plt.plot(time, values_time)
    plt.grid(True, linestyle="--", color="gray", linewidth="0.5")  # 加入网格
    # plt.tick_params(labelsize=8)  # 设置xy坐标刻度字体大小
    plt.xticks(fontsize=8)
    plt.savefig('用户发表短评数量随时刻的变化情况', dpi=600)
    print("用户发表短评数量随时刻的变化情况图表绘制完成，已保存！")

    list_scores_every_day = list(scores_every_day.items())
    list_scores_every_day.sort(key=lambda x: x[0], reverse=False)
    every_day, values_every_day = tuple_to_list(list_scores_every_day)
    every_day = translate(every_day, 5, 10)   # 去除日期中的年
    plt.figure(figsize=(16, 9))
    plt.title('随日期变化，评分变化情况', fontproperties='SimHei', fontsize=20)
    plt.xlabel("日期", fontproperties='SimHei', fontsize=20)
    plt.ylabel("评分(50为满分)", fontproperties='SimHei', fontsize=20)
    plt.plot(every_day, values_every_day)
    plt.grid(True, linestyle="--", color="gray", linewidth="0.5")  # 加入网格
    plt.xticks(fontsize=8)
    plt.savefig('随日期变化，评分变化情况', dpi=600)
    print("随日期变化，评分变化情况图表绘制完成，已保存！")


csv_data = pd.read_csv('热门电影影评数据爬取.csv', index_col='user_names')  # 读取文件，以user_names为列索引
counts_hao = jieba_fenci('推荐', '力荐')  # 好评分词
counts_zhong = jieba_fenci('还行')  # 中评分词
counts_cha = jieba_fenci('很差', '较差')  # 差评分词
counts_hao = remove_words(counts_hao)  # 去除停用词
counts_zhong = remove_words(counts_zhong)
counts_cha = remove_words(counts_cha)
words_counts()     # 词频统计
draw_wordcloud()   # 绘制词云
days_dict = times(0, 10)
times_dict = times(11, 13)
scores_every_day = scores_everyday()
hui_tu()
