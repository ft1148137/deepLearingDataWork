# -*- coding: UTF-8 -*-
import cv2
import math
import numpy as np
import os
import glob
import json
import shutil
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ElementTree, Element
from config import class_mirror_mode, class_ids, img_path_mirror, img_path_mirrored

def writeTxt(org_path,root):
    out_file = open(org_path[:-4] + '.txt','w')
    for obj in root.iter('object'):
        box = obj.find('bndbox') 
        b = (float(box.find('xmin').text), float(box.find('xmax').text), float(box.find('ymin').text),
        float(box.find('ymax').text))
        bn = convert((float(root.find('size').find('width').text),float(root.find('size').find('height').text)),b)
        out_file.write(str(class_ids[obj.find('name').text]) + " " + " ".join([str('%.6f' % a) for a in bn]) + '\n')
    pass

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

def h_MirrorImg(img_path,img_write_path):
    img = cv2.imread(img_path)
    mirror_img = cv2.flip(img, 1)  #
    cv2.imwrite(img_write_path,mirror_img)

def v_MirrorImg(img_path,img_write_path):
    img = cv2.imread(img_path)
    mirror_img = cv2.flip(img, 0)  #
    cv2.imwrite(img_write_path,mirror_img)

def a_MirrorImg(img_path,img_write_path):
    img = cv2.imread(img_path)
    mirror_img = cv2.flip(img, -1)  #
    cv2.imwrite(img_write_path,mirror_img)

def h_MirrorAnno(anno_path,anno_write_path):
    tree = ET.parse(anno_path)
    root = tree.getroot()
    size=root.find('size')
    w=int(size.find('width').text)
    objects = root.findall("object")
    for obj in objects:
        bbox = obj.find('bndbox')
        x1 = float(bbox.find('xmin').text)
        x2 = float(bbox.find('xmax').text)
        x1=w-x1+1
        x2=w-x2+1

        assert x1>0
        assert x2>0

        bbox.find('xmin').text=str(int(x2))
        bbox.find('xmax').text=str(int(x1))
    writeTxt(anno_write_path,root)
    tree.write(anno_write_path)  # 保存修改后的XML文件

def v_MirrorAnno(anno_path,anno_write_path):
    tree = ET.parse(anno_path)
    root = tree.getroot()
    size = root.find('size')
    h=int(size.find('height').text)
    objects = root.findall("object")
    for obj in objects:
        bbox = obj.find('bndbox')
        y1 = float(bbox.find('ymin').text)
        y2 = float(bbox.find('ymax').text)

        y1=h-y1+1
        y2=h-y2+1

        assert y1>0
        assert y2>0

        bbox.find('ymin').text=str(int(y2))
        bbox.find('ymax').text=str(int(y1))

    tree.write(anno_write_path)  # 保存修改后的XML文件

def a_MirrorAnno(anno_path,anno_write_path):
    tree = ET.parse(anno_path)
    root = tree.getroot()
    size = root.find('size')
    w=int(size.find('width').text)
    h = int(size.find('height').text)
    objects = root.findall("object")
    for obj in objects:
        bbox = obj.find('bndbox')
        x1 = float(bbox.find('xmin').text)
        y1 = float(bbox.find('ymin').text)
        x2 = float(bbox.find('xmax').text)
        y2 = float(bbox.find('ymax').text)

        x1=w-x1+1
        x2=w-x2+1

        y1 = h - y1+1
        y2 = h - y2+1

        assert x1 > 0
        assert x2 > 0
        assert y1 > 0
        assert y2 > 0

        bbox.find('xmin').text=str(int(x2))
        bbox.find('xmax').text=str(int(x1))
        bbox.find('ymin').text=str(int(y2))
        bbox.find('ymax').text=str(int(y1))

    tree.write(anno_write_path)  # 保存修改后的XML文件

def mirror(img_dir,anno_dir,img_write_dir,anno_write_dir):
    if not os.path.exists(img_write_dir):
        os.makedirs(img_write_dir)

    if not os.path.exists(anno_write_dir):
        os.makedirs(anno_write_dir)
    img_names=os.listdir(img_dir)
    for img_name in img_names:
        if img_name.endswith('.png'):
            img_path=os.path.join(img_dir,img_name)
            h_img_write_path=os.path.join(img_write_dir,img_name[:-4]+'h'+'.png')
            anno_path=os.path.join(anno_dir,img_name[:-4]+'.xml')
            h_anno_write_path = os.path.join(anno_write_dir, img_name[:-4]+'h'+'.xml')
            #
            # v_img_write_path = os.path.join(img_write_dir, img_name[:-4] + 'v' + '.png')
            # v_anno_write_path = os.path.join(anno_write_dir, img_name[:-4] + 'v' + '.xml')
            #
            # a_img_write_path = os.path.join(img_write_dir, img_name[:-4] + 'a' + '.png')
            # a_anno_write_path = os.path.join(anno_write_dir, img_name[:-4] + 'a' + '.xml')
            #
            h_MirrorImg(img_path,h_img_write_path)
            # v_MirrorImg(img_path,v_img_write_path)
            # a_MirrorImg(img_path, a_img_write_path)
            h_MirrorAnno(anno_path,h_anno_write_path)
            # v_MirrorAnno(anno_path, v_anno_write_path)
            # a_MirrorAnno(anno_path, a_anno_write_path)


if __name__ == '__main__':
    if not os.path.exists(img_path_mirrored):
        os.mkdir(img_path_mirrored)
    for classname in class_mirror_mode.keys():
        if not os.path.exists(os.path.join(img_path_mirror,classname)):
            print("no",classname,"file in the path,check next class")
            continue
        if not os.path.exists(os.path.join(img_path_mirrored,classname)):
            os.mkdir(os.path.join(img_path_mirrored,classname))
        print("working on",classname)
        mirror(img_path_mirror + '/' + classname, img_path_mirror + '/' + classname, img_path_mirrored + '/' + classname, img_path_mirrored + '/' + classname)