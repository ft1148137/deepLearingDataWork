import cv2
import numpy as np
import os
import xml.etree.ElementTree as ET

from config import img_path_color_transform, img_path_color_transformed, class_color_transform_mode, clahe_img_ksize, brightness_diff

def hisColor_Img(org_path,dir_path):
    img = cv2.imread(org_path,cv2.CV_8UC1)
    img_eq = cv2.equalizeHist(img)
    cv2.imwrite(dir_path,img_eq);
    pass

def clahe_Img(org_path,dir_path,ksize):
    image = cv2.imread(org_path, cv2.IMREAD_COLOR)
    b, g, r = cv2.split(image)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(ksize,ksize))
    b = clahe.apply(b)
    g = clahe.apply(g)
    r = clahe.apply(r)
    image = cv2.merge([b, g, r])
    cv2.imwrite(dir_path,image);

def brightness_Img(org_path,dir_path,brightness):
    img = cv2.imread(org_path)
    imgHeight,imgWidth,imgDeep = img.shape
    trans_img = np.zeros((imgHeight, imgWidth, 1), np.uint8)
    for i in range(0, imgHeight):
        for j in range(0, imgWidth):
            a,b,intensity = map(int,img[i,j])
            intensity += brightness
            if intensity > 255:
                intensity = 255
            trans_img[i, j] = intensity
    cv2.imwrite(dir_path,trans_img);

def write_label(anno_path,anno_write_path):
    tree = ET.parse(anno_path)
    tree.write(anno_write_path)

def color_transform(classname,img_dir,anno_dir,img_write_dir,anno_write_dir):
    if not os.path.exists(img_write_dir):
        os.makedirs(img_write_dir)

    if not os.path.exists(anno_write_dir):
        os.makedirs(anno_write_dir)
    img_names=os.listdir(img_dir)
    for img_name in img_names:
        if img_name.endswith('.png'):
            if(class_color_transform_mode[classname][0] == True):
                img_path=os.path.join(img_dir,img_name)
                img_write_path=os.path.join(img_write_dir,img_name[:-4]+'hiscolor'+'.png')
                anno_path=os.path.join(anno_dir,img_name[:-4]+'.xml')
                anno_write_path = os.path.join(anno_write_dir, img_name[:-4]+'hiscolor'+'.xml')
                hisColor_Img(img_path,img_write_path)
                write_label(anno_path,anno_write_path)

            if(class_color_transform_mode[classname][1] == True):
                img_path=os.path.join(img_dir,img_name)
                img_write_path=os.path.join(img_write_dir,img_name[:-4]+'clahe'+'.png')
                anno_path=os.path.join(anno_dir,img_name[:-4]+'.xml')
                anno_write_path = os.path.join(anno_write_dir, img_name[:-4]+'clahe'+'.xml')
                clahe_Img(img_path,img_write_path,clahe_img_ksize)
                write_label(anno_path,anno_write_path)

            if(class_color_transform_mode[classname][2] == True):
                img_path=os.path.join(img_dir,img_name)
                img_write_path=os.path.join(img_write_dir,img_name[:-4]+'brightness'+'.png')
                anno_path=os.path.join(anno_dir,img_name[:-4]+'.xml')
                anno_write_path = os.path.join(anno_write_dir, img_name[:-4]+'brightness'+'.xml')
                brightness_Img(img_path,img_write_path,brightness_diff)
                write_label(anno_path,anno_write_path)

if __name__ == "__main__":
    if not os.path.exists(img_path_color_transformed):
            os.mkdir(img_path_color_transformed)
    for classname in class_color_transform_mode.keys():
        if not os.path.exists(os.path.join(img_path_color_transform,classname)):
            print("no",classname,"file in the path,check next class")
            continue
        if not os.path.exists(os.path.join(img_path_color_transformed,classname)):
            os.mkdir(os.path.join(img_path_color_transformed,classname))
        print("working on",classname)
        color_transform(classname,img_path_color_transform + '/' + classname, img_path_color_transform + '/' + classname, img_path_color_transformed + '/' + classname, img_path_color_transformed + '/' + classname)
    pass

