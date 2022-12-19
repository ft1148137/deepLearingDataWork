#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import cv2
from skimage.measure import compare_ssim
import shutil
import time
import numpy as np
from joblib import Parallel, delayed
import multiprocessing

filterting = 0 ## 0 auto filtering, 1 manual filtering
auto_filterting_thr = 0.9
def move(name,dir):
    shutil.move(name,dir)
def delete(filename1):
    os.remove(filename1)

def ssim(img1, img2):
    C1 = (0.01 * 255)**2
    C2 = (0.03 * 255)**2
    img1 = img1.astype(np.float64)
    img2 = img2.astype(np.float64)
    kernel = cv2.getGaussianKernel(11, 1.5)
    window = np.outer(kernel, kernel.transpose())
    mu1 = cv2.filter2D(img1, -1, window)[5:-5, 5:-5] # valid
    mu2 = cv2.filter2D(img2, -1, window)[5:-5, 5:-5]
    mu1_sq = mu1**2
    mu2_sq = mu2**2
    mu1_mu2 = mu1 * mu2
    sigma1_sq = cv2.filter2D(img1**2, -1, window)[5:-5, 5:-5] - mu1_sq
    sigma2_sq = cv2.filter2D(img2**2, -1, window)[5:-5, 5:-5] - mu2_sq
    sigma12 = cv2.filter2D(img1 * img2, -1, window)[5:-5, 5:-5] - mu1_mu2
    ssim_map = ((2 * mu1_mu2 + C1) * (2 * sigma12 + C2)) / ((mu1_sq + mu2_sq + C1) *
                                (sigma1_sq + sigma2_sq + C2))
    return ssim_map.mean()

def calculate_ssim(img1, img2):
    if not img1.shape == img2.shape:
        raise ValueError('Input images must have the same dimensions.')
    if img1.ndim == 2:
        return ssim(img1, img2)
    elif img1.ndim == 3:
        if img1.shape[2] == 3:
            ssims = []
            for i in range(3):
                ssims.append(ssim(img1, img2))
            return np.array(ssims).mean()
        elif img1.shape[2] == 1:
            return ssim(np.squeeze(img1), np.squeeze(img2))
    else:
        raise ValueError('Wrong input image dimensions.')


def ssim_speed_up(currIndex,img_files):
    print("index now",currIndex+1,"/",len(img_files))
    del_list = []
    img = cv2.imread(img_files[currIndex],cv2.CV_8UC1)
    img = cv2.resize(img, (64, 48), interpolation=cv2.INTER_LINEAR)
    for dirIndex in range(currIndex+1,len(img_files)):
        img1 = cv2.imread(img_files[dirIndex],cv2.CV_8UC1)
        img1 = cv2.resize(img1, (64, 48), interpolation=cv2.INTER_LINEAR)
        ssim = calculate_ssim(img,img1)                 
        if ssim > auto_filterting_thr:
            if(img_files[currIndex] not in del_list):
                del_list.append(img_files[currIndex])
                shutil.copyfile(img_files[dirIndex],os.path.join(dir_path,(img_files[currIndex].split("/")[-1])[:-4]+"c"+str(round(ssim,2))+".png"))
                print(img_files[currIndex],img_files[dirIndex],ssim)
                continue
                print('---------------------------------------------------------------');
    return(del_list)

def show_in_one(images):
    show_size=(480*2+4, 640*2+4)
    blank_size=2
    window_name="merge"
    small_h, small_w = images[0].shape[:2]
    column = int(show_size[1] / (small_w + blank_size))
    row = int(show_size[0] / (small_h + blank_size))
    shape = [show_size[0], show_size[1]]
    for i in range(2, len(images[0].shape)):
        shape.append(images[0].shape[i])

    merge_img = np.zeros(tuple(shape), images[0].dtype)

    max_count = len(images)
    count = 0
    for i in range(row):
        for j in range(column):
            if count < max_count:
                im = images[count]
                t_h_start = i * (small_h + blank_size)
                t_w_start = j * (small_w + blank_size)
                t_h_end = t_h_start + im.shape[0]
                t_w_end = t_w_start + im.shape[1]
                merge_img[t_h_start:t_h_end, t_w_start:t_w_end] = im
                count = count + 1

    cv2.namedWindow(window_name)
    cv2.imshow(window_name, merge_img)
    while(True):
        key = cv2.waitKey(10);
        if(key == 100):
            return True
        elif (key!=-1):
            break
    return False

def maunal_fliter(img_files):
    del_list = []
    for currIndex in range(len(img_files)):
        img = cv2.imread(img_files[currIndex],cv2.CV_8UC1)
        dirIndex = currIndex+1
        while dirIndex < len(img_files) -3:
            img_list = [img]
            for i in range(3):
                img2 = cv2.imread(img_files[dirIndex+i],cv2.CV_8UC1)
                img_list.append(img2)
            dirIndex += 3
            print("dir index:",dirIndex)
            if show_in_one(img_list):
                shutil.copyfile(img_files[dirIndex],os.path.join(dir_path,(img_files[currIndex].split("/")[-1])[:-4]+"c"+".png"))
                shutil.move(img_files[currIndex],dir_path)
                print("delete img")
                break
    return(del_list)

if __name__ == '__main__':
    path = './data/qfeel_detect/10_data_2022_12_09/img'
    dir_path = './data/qfeel_detect/10_data_2022_12_09/moved'
    # path = './images'
    # dir_path = './images/moved'
    files = os.listdir(path)
    img_files = [os.path.join(path,file) for file in files if file.endswith('.png')]    
    if(not os.path.exists(dir_path)):
        os.mkdir(dir_path)
    else:
        shutil.rmtree(dir_path)
        os.mkdir(dir_path)
    if filterting == 0:
        num_cores = multiprocessing.cpu_count()
        print("num core:",num_cores)
        del_list = Parallel(n_jobs=num_cores)(delayed(ssim_speed_up)(currIndex,img_files) for currIndex in range(len(img_files)))
        cnt = 0
        if(len(del_list) > 0):
            for list in del_list:
                for image in list:
                    cnt+=1
                    if not os.path.exists(os.path.join(dir_path,image.split("/")[-1])):
                        shutil.move(image,dir_path)
                    #delete(image)
                    print('delete',image)
        print('delte sum:',cnt)
    elif filterting == 1:
        maunal_fliter(img_files)
