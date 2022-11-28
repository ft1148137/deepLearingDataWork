# -*- coding: UTF-8 -*-
'''
1. 统计每一个类别有几个标注（一张图片中如果某个类型有多个，将会统计多个）
2. 统计标注总数
3. 绘制类别中标记数目图
'''

import os
import xml.dom.minidom
from config import class_name_proj, annopath_count

Annolist = os.listdir(annopath_count)
anno_list_xml = [x for x in Annolist if x[-4:] == '.xml']
rate = {} # 创建一个字典用于存放标签名和对应的出现次数
data_total = 0
objet_total = 0
background_total = 0

for annotation in anno_list_xml:
    fullname = annopath_count + annotation
    if not os.path.getsize(fullname):
        background_total += 1
        continue
    else:
        dom = xml.dom.minidom.parse(fullname) # 打开XML文件
        data_total += 1
        collection = dom.documentElement # 获取元素对象
        objectlist = collection.getElementsByTagName('object') # 获取标签名为object的信息
        for object in objectlist:
            namelist = object.getElementsByTagName('name') # 获取子标签name的信息
            objectname = class_name_proj[namelist[0].childNodes[0].data] if namelist[0].childNodes[0].data in class_name_proj.keys() else namelist[0].childNodes[0].data
            if objectname not in rate: # 判断字典里有没有标签，如无添加相应字段
                rate[objectname] = 0
            rate[objectname] += 1
            objet_total += 1

print(rate)
print('data_total:', data_total)
print('objet_total:', objet_total)
print('background_total:', background_total)

'''
#画图
import matplotlib.pyplot as plt
# object = []
# number = []
# for key in rate:
#     object.append(key)
#     number.append(rate[key])
# plt.figure()
# #解决中文显示问题
# plt.rcParams['font.sans-serif']=['SimHei']
# plt.rcParams['axes.unicode_minus'] = False
# plt.bar(object, number)
# # plt.bar(number,object )
#
# plt.title('result')
# plt.show()
#########################################
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus'] = False
fig, ax = plt.subplots()
b = ax.barh(range(len(keys)), values, color='#6699CC')

# 为横向水平的柱图右侧添加数据标签。
for rect in b:
    w = rect.get_width()
    ax.text(w, rect.get_y() + rect.get_height() / 2, '%d' %
            int(w), ha='left', va='center')

# 设置Y轴纵坐标上的刻度线标签。
ax.set_yticks(range(len(keys)))
ax.set_yticklabels(keys)

# 不要X横坐标上的label标签。
plt.xticks(())

plt.title('num_class', loc='center', fontsize='25',
          fontweight='bold', color='k')
plt.savefig(r'./count.jpg')
plt.show()
'''