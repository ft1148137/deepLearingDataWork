# -*- coding: UTF-8 -*-
# 读取图片，读取xml文件
# 解析xml文件获取图片的大小，xml中的多组坐标
# 翻转图片，根据图片翻转的角度，获取新的图片大小和坐标点
# 将坐标信息和图片大小在原有的xml中修改参数保存到新的xml和txt文件中
# 创建新的文件夹，将图片和xml文件放在同一文件夹中（一组图片和xml文件命名相同）

import os
import numpy as np
import cv2
import math
import xml.etree.ElementTree as ET
from config import class_ids, class_rotation_angle, img_path_rotation, img_path_rotated

def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)       

# 按角度翻转图片
def rotate_img(src, angle, scale=1):
    width = src.shape[1]
    height = src.shape[0]
    # 角度变弧度
    re_angle = np.deg2rad(angle)
    # 计算新图片的高度和宽度
    new_width = (abs(np.sin(re_angle) * height) + abs(np.cos(re_angle) * width)) * scale
    new_height = (abs(np.cos(re_angle) * height) + abs(np.sin(re_angle) * width)) * scale

    rotate_matrix = cv2.getRotationMatrix2D((new_width * 0.5, new_height * 0.5), angle, scale)
    rotate_move = np.dot(rotate_matrix, np.array([(new_width - width) * 0.5, (new_height - height) * 0.5, 0]))

    # update translation
    rotate_matrix[0, 2] += rotate_move[0]
    rotate_matrix[1, 2] += rotate_move[1]

    dst = cv2.warpAffine(img, rotate_matrix, (int(math.ceil(new_width)), int(math.ceil(new_height))),
                         flags=cv2.INTER_LANCZOS4)
    return dst

def rotate_xy(x, y, angle, cx, cy):  
    angle_ = angle * np.pi / 180
    x_new = (x - cx) * math.cos(angle_) - (y - cy) * math.sin(angle_) + cx     
    y_new = (x - cx) * math.sin(angle_) + (y - cy) * math.cos(angle_) + cy     
    return [x_new,y_new,cx, cy]   

# 翻转后的xml文件信息
def rotate_xml(src, xmin, ymin, xmax, ymax, angle, scale=1):
    width = src.shape[1]
    height = src.shape[0]
    re_angle = np.deg2rad(angle)
    new_width = (abs(np.sin(re_angle) * height) + abs(np.cos(re_angle) * width)) * scale
    new_height = (abs(np.cos(re_angle) * height) + abs(np.sin(re_angle) * width)) * scale
    rotate_matrix = cv2.getRotationMatrix2D((new_width * 0.5, new_height * 0.5), angle, scale)
    rotate_move = np.dot(rotate_matrix, np.array([(new_width - width) * 0.5, (new_height - height) * 0.5, 0]))
    rotate_matrix[0, 2] += rotate_move[0]
    rotate_matrix[1, 2] += rotate_move[1]
    # 获取原始矩形的四个中点，然后将这四个点转换到旋转后的坐标系下
    point1 = np.dot(rotate_matrix, np.array([(xmin + xmax) / 2, ymin, 1]))
    point2 = np.dot(rotate_matrix, np.array([xmax, (ymin + ymax) / 2, 1]))
    point3 = np.dot(rotate_matrix, np.array([(xmin + xmax) / 2, ymax, 1]))
    point4 = np.dot(rotate_matrix, np.array([xmin, (ymin + ymax) / 2, 1]))
    concat = np.vstack((point1, point2, point3, point4))  # 合并np.array
    # 改变array类型
    concat = concat.astype(np.int32)
    rx, ry, rw, rh = cv2.boundingRect(concat)  # rx,ry,为新的外接框左上角坐标，rw为框宽度，rh为高度
    new_xmin = rx
    new_ymin = ry
    new_xmax = rx + rw
    new_ymax = ry + rh

    return new_xmin, new_ymin, new_xmax, new_ymax


if __name__ == '__main__':
    
    # 自定义翻转角度
    if not os.path.exists(img_path_rotated):
        os.mkdir(img_path_rotated)
    for classname in class_rotation_angle.keys():
        if not os.path.exists(os.path.join(img_path_rotation,classname)):
            print("no",classname,"file in the path,check next class")
            continue
        if not os.path.exists(os.path.join(img_path_rotated,classname)):
            os.mkdir(os.path.join(img_path_rotated,classname))
        for angle in class_rotation_angle[classname]:
            print("working on",classname," rotated",angle)
            for file in os.listdir(os.path.join(img_path_rotation,classname)):
                a, b = os.path.splitext(file)
                if file.endswith('.png'):
                    img = cv2.imread(img_path_rotation  + classname + "/"+ a + '.png')
                    rotated_img = rotate_img(img, angle)
                    cv2.imwrite(img_path_rotated + classname + "/"+ a + str(angle) + '.png', rotated_img)
                if file.endswith('.xml'):
                    src = cv2.imread(img_path_rotation + classname + "/" + a + '.png')
                    tree = ET.parse(img_path_rotation + classname + "/" + a + '.xml')
                    root = tree.getroot()
                    if angle in (90, 270, 450):
                        for size in root.iter('size'):
                            size.find('width').text = str(480)
                            size.find('height').text = str(640)
                    out_file = open(img_path_rotated + classname + "/"+ a + str(angle) + '.txt','w')
                ## 修改xml中的标签坐标信息
                    for obj in root.iter('object'):
                        box = obj.find('bndbox') 
                        xmin = float(box.find('xmin').text)
                        ymin = float(box.find('ymin').text)
                        xmax = float(box.find('xmax').text)
                        ymax = float(box.find('ymax').text)
                        new_xmin, new_ymin, new_xmax, new_ymax = rotate_xml(src, xmin, ymin, xmax, ymax, angle)
                        box.find('xmin').text = str(new_xmin)
                        box.find('ymin').text = str(new_ymin)
                        box.find('xmax').text = str(new_xmax)
                        box.find('ymax').text = str(new_ymax)
                        b = (float(box.find('xmin').text), float(box.find('xmax').text), float(box.find('ymin').text),
                        float(box.find('ymax').text))
                        bn = convert((float(root.find('size').find('width').text),float(root.find('size').find('height').text)),b)
                        out_file.write(str(class_ids[obj.find('name').text]) + " " + " ".join([str('%.6f' % a) for a in bn]) + '\n')
                    tree.write(img_path_rotated + classname + "/"+ a + str(angle) + '.xml')

    print("-----------------------------------")
    print("Successful!")