# -*- coding: utf-8 -*-
# author:           inspurer(月小水长)
# pc_type           lenovo
# create_date:      2019/3/2
# file_name:        data_analysis.py
# github            https://github.com/inspurer
# qq_mail           2391527690@qq.com
# 微信公众号         月小水长(ID: inspurer)

from configure import *
from pymongo import MongoClient

import matplotlib.pyplot as plt
import matplotlib


# 设置中文字体和负号正常显示
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

class dataAnalysis(object):

    def __init__(self):
        self.client = MongoClient(MONGO_URL, connect=False)
        self.db = self.client[MONGO_DB]
        self.table = self.db[MONGO_TABLE]
        self.raw_data = self.table.find()
        print(self.raw_data.count())
        # for result in results:
        #     print(result)
        pass

    def age_counter(self):
        self.age_dict = dict()
        for line in self.raw_data:
            age = line.get('age')
            if age not in self.age_dict.keys():
                self.age_dict[age] = 1
            else:
                self.age_dict[age] +=1
        print(self.age_dict)

    def wordcloud_util(self):
        all_sign = ""
        for line in self.table.find():
            sign = line.get('nickname')
            all_sign = all_sign + sign + "\n"
        if os.path.exists("wc/sign.txt"):
            os.remove("wc/sign.txt")
        with open("wc/sign.txt","a+",encoding="utf-8") as f:
            f.write(all_sign)

    def data_viewer(self):
        age_list = sorted((list)(self.age_dict.keys()))


        number =list()

        for age in age_list:
            number.append(self.age_dict.get(age))

        x = range(len(number))
        """
        绘制条形图
        left: 长条形中点横坐标
        height: 长条形高度
        width: 长条形宽度，默认值0
        .8
        label: 为后面设置legend准备
        """
        rects1 = plt.bar(x=x, height=number, width=0.5, alpha=0.8, color='#1ABDE6', label="直方图")

        plt.plot(age_list,number,color='#0066ff',label="折线图",linewidth = 1,marker='*',markersize=10)
        # plt.ylim(0, 50) # y轴取值范围
        plt.ylabel("人数/人")
        """
        设置x轴刻度显示值
        参数一：中点坐标
        参数二：显示值
        """
        plt.xticks(x, age_list)
        plt.xlabel("年龄")
        plt.title("uki 活跃用户各年龄人数直方-折线图")
        plt.legend()  # 设置题注 # 编辑文本
        for rect in rects1:
            height = rect.get_height()
            plt.text(rect.get_x() + rect.get_width() / 2, height + 1, str(height), ha="center", va="bottom")
        #plt.show()

        plt.figure()


        # 饼状图
        labels = ['10-15岁','15-20岁','20-25岁','25-30岁','其它']
        ages_dict = dict.fromkeys(labels,0)
        for key in self.age_dict.keys():
            age = int(key)
            if age >= 10 and age < 15:
                ages_dict['10-15岁'] += self.age_dict.get(key)
            elif age >= 15 and age < 20:
                ages_dict['15-20岁'] += self.age_dict.get(key)
            elif age >= 20 and age < 25:
                ages_dict['20-25岁'] += self.age_dict.get(key)
            elif age >= 25 and age < 30:
                ages_dict['25-30岁'] += self.age_dict.get(key)
            else:
                ages_dict['其它'] += self.age_dict.get(key)

        total = self.raw_data.count()

        explode = [0 for i in range(len(labels))]  # 0.1 凸出这部分，
        max = 0
        index = 0
        percentage = []
        for i,label in enumerate(labels):
            if ages_dict[label] > max:
                max = ages_dict[label]
                index = i
            percentage.append(ages_dict[label]/total)
        explode[index] = 0.1

        plt.axes(aspect=1)  # set this , Figure is round, otherwise it is an ellipse
        # autopct ，show percet
        plt.pie(x=percentage, labels=labels, explode=explode, autopct='%3.1f %%',
                shadow=True, labeldistance=1.1, startangle=90, pctdistance=0.6
                )
        plt.legend(loc='best')
        plt.title("uki 活跃用户年龄段比例图")
        '''
        labeldistance，文本的位置离远点有多远，1.1指1.1倍半径的位置
        autopct，圆里面的文本格式，%3.1f%%表示小数有三位，整数有一位的浮点数
        shadow，饼是否有阴影
        startangle，起始角度，0，表示从0开始逆时针转，为第一块。一般选择从90度开始比较好看
        pctdistance，百分比的text离圆心的距离
        patches, l_texts, p_texts，为了得到饼图的返回值，p_texts饼图内部文本的，l_texts饼图外label的文本
        '''

        plt.show()

    def main(self):
        self.age_counter()
        self.wordcloud_util()
        self.data_viewer()

if __name__ == '__main__':
    dataanalysis = dataAnalysis()
    dataanalysis.main()