import matplotlib.pyplot as plt
from scipy import signal
import numpy as np
import copy as cp
import random
import math
import cv2
import collections


#求两个点的差值
def getGrayDiff(image,currentPoint,tmpPoint):
    return abs(int(image[currentPoint[0],currentPoint[1]]) - int(image[tmpPoint[0],tmpPoint[1]]))

#区域生长算法
def regional_growth (gray,seeds,threshold=15) :
    #每次区域生长的时候的种子像素之间的八个邻接点
    connects = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), \
                        (0, 1), (-1, 1), (-1, 0)]    
    threshold = threshold #种子生长时候的相似性阈值，默认即灰度级不相差超过15以内的都算为相同
    height, weight = gray.shape
    seedMark = np.zeros(gray.shape)
    seedList = []
    for seed in seeds:
        seedList.append(seed)   #将种子添加到种子的列表中
    label = 1	#标记点的flag
    while(len(seedList)>0):     #如果种子列表里还存在种子点
        currentPoint = seedList.pop(0)  #将最前面的那个种子抛出
        if currentPoint[0]>=height or currentPoint[1]>=weight:
            break

        seedMark[currentPoint[0],currentPoint[1]] = label   #将对应位置的点标志为1
        for i in range(8):  #对这个种子点周围的8个点一次进行相似性判断
            tmpX = currentPoint[0] + connects[i][0]
            tmpY = currentPoint[1] + connects[i][1]
            if tmpX < 0 or tmpY < 0 or tmpX >= height or tmpY >= weight:    #如果超出限定的阈值范围
                continue    #跳过并继续
            grayDiff = getGrayDiff(gray,currentPoint,(tmpX,tmpY))   #计算此点与种子像素点的灰度级之差
            if grayDiff < threshold and seedMark[tmpX,tmpY] == 0:
                seedMark[tmpX,tmpY] = label
                seedList.append((tmpX,tmpY))
    return seedMark

def MAIN(): 
    image = cv2.imread('part1.png')
    cv2.imshow("color_image",image)
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

    #cv2.imshow("gray_img",gray)
    
    seed_points = [(50,50)]  #输入选取的种子像素
    seed_grow_image = regional_growth(gray,seed_points,5)
    cv2.imshow('region_growth',seed_grow_image)
    cv2.waitKey(0)


if __name__ == "__main__":
    MAIN()
