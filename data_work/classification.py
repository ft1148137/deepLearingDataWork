# -*- coding: UTF-8 -*-
'''
1. 将混在一起的数据集按照类别分类，如果一张图片中有两种类型，则会同时被分到两类中。
2. 统计每一个类别有几个标注（一张图片中如果某个类型有多个，将会统计多个）
3. 统计标注总数
'''

import os
import shutil
import xml.dom.minidom
from PIL import Image
from config import class_name_proj, annopath_classification, \
                img_path_classification, txt_label_path_classification, dir_path_classification

root_dir = os.path.dirname(__file__)
images_path = os.path.join(root_dir, dir_path_classification)


for class_name in class_name_proj.values():
    class_dir = os.path.join(images_path, class_name)
    if  not os.path.exists(class_dir):
        os.makedirs(class_dir)
#-------------------------------------------------------------------------#
Annolist = os.listdir(annopath_classification)
rate = {} # 创建一个字典用于存放标签名和对应的出现次数
total = 0

for annotation in Annolist:
    if annotation[-4:] != ".xml":
        continue
    fullname = annopath_classification + annotation[0:-4] + ".xml"
    image_name =  annotation[0:-4]
    if not os.path.getsize(fullname):
        continue
    else:
        dom = xml.dom.minidom.parse(fullname) # 打开XML文件
        # print(fullname,annotation)
        print('---------------total:', total,'--------------------')

        collection = dom.documentElement # 获取元素对象
        objectlist = collection.getElementsByTagName('object') # 获取标签名为object的信息
        for object in objectlist:
            namelist = object.getElementsByTagName('name') # 获取子标签name的信息
            objectname = namelist[0].childNodes[0].data # 取到name具体的值
            objectname_path = class_name_proj[objectname]
            
            if objectname not in rate: # 判断字典里有没有标签，如无添加相应字段
                rate[objectname] = 0

    #----------------------拷贝图片到对应目录------------------------#
            image_path = img_path_classification + '/' + image_name+".png"
            if os.path.exists(image_path):
                image = Image.open(image_path)
                image.save(os.path.join(images_path, objectname_path) +'/'+image_name+".png")
    #----------------------拷贝xml文件到对应目录------------------------#
            anno_path = annopath_classification + image_name+".xml"
            if os.path.exists(anno_path):
                old = os.path.join(images_path, objectname_path)+'/'+image_name+".xml"
                shutil.copyfile(anno_path, old)
    # ----------------------拷贝txt文件到对应目录------------------------#
            txtlabel_path = txt_label_path_classification + image_name + ".txt"
            if os.path.exists(txtlabel_path):
                old = os.path.join(images_path, objectname_path) + '/' + image_name + ".txt"
                shutil.copyfile(txtlabel_path, old)

            rate[objectname] += 1
            total += 1


print(rate)
print('total:', total)