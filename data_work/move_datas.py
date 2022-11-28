# -*- coding: UTF-8 -*-
import os
import random
import shutil

classnames_ =  {'cable':0,
                'carpet_boundary':1000,
                'carpet_fringe':2000,
                'cheerios':2000,
                'dock':2000,
                'furniture_leg':0,
                'shoe':0,
                'threshold':2000}

# file_path_ = '../Classification/imgs_class/'
file_path_ = '../Classification/Data_Augmentation/'
dest_path_ = '../datasetOrdered/'

def move(filepath, dirpath,size):
    if(not os.path.exists(dirpath)):
        os.mkdir(dirpath)
    image_path = os.path.join(dirpath,'images')
    label_path = os.path.join(dirpath,'labels')
    if(not os.path.exists(image_path)):
            os.mkdir(image_path)
    if(not os.path.exists(label_path)):
            os.mkdir(label_path)
    pathdir = os.listdir(filepath)
    imagenames = [x for x in pathdir if x[-4:] == '.png']
    real_size = min(size,len(imagenames))
    ranpath = random.sample(imagenames, int(real_size))
    cout = 0
    for alldir in ranpath:
        org = os.path.join(filepath, alldir)
        dest = os.path.join(image_path, alldir)
        if(not os.path.exists(os.path.join(image_path, alldir))):
            if not os.path.exists(dest):
                shutil.copy(org, dest)
            org = os.path.join(filepath, alldir[0:-4]+".txt")
            dest = os.path.join(label_path, alldir[0:-4]+".txt")
            if not os.path.exists(dest):
                shutil.copy(org, dest)
            org = os.path.join(filepath, alldir[0:-4]+".xml")
            dest = os.path.join(label_path, alldir[0:-4]+".xml")
            if not os.path.exists(dest):
                shutil.copy(org, dest)
            cout+=1
    print("-------------------move finish, moved ",cout," images")

if __name__ == "__main__":
    for classname in classnames_.keys():
        print("moving ",classnames_[classname]," ",classname,"....")
        imgpath = os.path.join(file_path_, classname)
        move(imgpath, dest_path_,classnames_[classname])

