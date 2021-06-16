from __future__ import print_function
import sys
import cv2
from random import randint
import numpy as np


trackerTypes = ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']

#求两个点的差值
def getGrayDiff(image,currentPoint,tmpPoint):
    return abs(int(image[currentPoint[0],currentPoint[1]]) - int(image[tmpPoint[0],tmpPoint[1]]))

#区域生长算法
def regional_growth (y1,y2,x1,x2,frame,gray,seeds,threshold=15) :
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
            continue

        seedMark[currentPoint[0],currentPoint[1]] = label   #将对应位置的点标志为1
        frame[currentPoint[0],currentPoint[1]]=(0,0,255)
        for i in range(8):  #对这个种子点周围的8个点一次进行相似性判断
            tmpX = currentPoint[0] + connects[i][0]
            tmpY = currentPoint[1] + connects[i][1]
            if tmpX < y1 or tmpY < x1 or tmpX >= y2 or tmpY >= x2:    #如果超出限定的阈值范围
                continue    #跳过并继续
            grayDiff = getGrayDiff(gray,currentPoint,(tmpX,tmpY))   #计算此点与种子像素点的灰度级之差
            if grayDiff < threshold and seedMark[tmpX,tmpY] == 0:
                seedMark[tmpX,tmpY] = label
                seedList.append((tmpX,tmpY))
    return seedMark

def createTrackerByName(trackerType):
        # Create a tracker based on tracker name
        if trackerType == trackerTypes[0]:
            tracker = cv2.legacy.TrackerBoosting_create()
        elif trackerType == trackerTypes[1]:
            tracker = cv2.legacy.TrackerMIL_create()
        elif trackerType == trackerTypes[2]:
            tracker = cv2.legacy.TrackerKCF_create()
        elif trackerType == trackerTypes[3]:
            tracker = cv2.legacy.TrackerTLD_create()
        elif trackerType == trackerTypes[4]:
            tracker = cv2.legacy.TrackerMedianFlow_create()
        elif trackerType == trackerTypes[5]:
            tracker = cv2.legacy.TrackerGOTURN_create()
        elif trackerType == trackerTypes[6]:
            tracker = cv2.TrackerMOSSE_create()
        elif trackerType == trackerTypes[7]:
            tracker = cv2.legacy.TrackerCSRT_create()
        else:
            tracker = None
            print('Incorrect tracker name')
            print('Available trackers are:')
            for t in trackerTypes:
                print(t)

        return tracker





# Set video to load
videoPath = "in.mp4"

# Create a video capture object to read videos
cap = cv2.VideoCapture(videoPath)

# Read first frame
success, frame = cap.read()
# quit if unable to read the video file

# part1 = frame[161:161+113,140:140+111 ]#y1:y2, x1:x2
# cv2.imwrite("part1.jpg",part1)

# part1 = frame[343:343+81,282:282+80 ]#y1:y2, x1:x2
# cv2.imwrite("part2.jpg",part1)

if not success:
  print('Failed to read video')
  sys.exit(1)

  ## Select boxes
bboxes = [(160,181,80,80),(282, 343, 80, 81)]#(最小x,最小y，宽，高)
colors = [(randint(0, 255), randint(0, 255), randint(0, 255)),(randint(0, 255), randint(0, 255), randint(0, 255))] 

# OpenCV's selectROI function doesn't work for selecting multiple objects in Python
# So we will call this function in a loop till we are done selecting all objects

#get bbox
# while True:
#   # draw bounding boxes over objects
#   # selectROI's default behaviour is to draw box starting from the center
#   # when fromCenter is set to false, you can draw box starting from top left corner
#   bbox = cv2.selectROI('MultiTracker', frame)
#   bboxes.append(bbox)
#   colors.append((randint(0, 255), randint(0, 255), randint(0, 255)))
#   print("Press q to quit selecting boxes and start tracking")
#   print("Press any other key to select next object")
#   k = cv2.waitKey(0) & 0xFF
#   print(k)
#   if (k == 113):  # q is pressed
#     break

height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
out = cv2.VideoWriter("outputColored.mp4", cv2.VideoWriter_fourcc('D', 'I', 'V', 'X'), 15,
                (np.int(width), np.int(height)), True)


print('Selected bounding boxes {}'.format(bboxes))

# Specify the tracker type
trackerType = "CSRT"
#trackerType = "BOOSTING"
createTrackerByName(trackerType)

# Create MultiTracker object
multiTracker = cv2.legacy.MultiTracker_create()


# Initialize MultiTracker 
for bbox in bboxes:
  multiTracker.add(createTrackerByName(trackerType), frame, bbox)


 
# # Setup SimpleBlobDetector parameters.
# params = cv2.SimpleBlobDetector_Params()
 
# # Change thresholds
# params.minThreshold = 10
# params.maxThreshold = 200
 
 
# # Filter by Area.
# params.filterByArea = True
# params.minArea = 1500
 
# # Filter by Circularity
# params.filterByCircularity = True
# params.minCircularity = 0.1
 
# # Filter by Convexity
# params.filterByConvexity = True
# params.minConvexity = 0.87
    
# # Filter by Inertia
# params.filterByInertia = True
# params.minInertiaRatio = 0.01
 
# # Create a detector with the parameters
# ver = (cv2.__version__).split('.')
# if int(ver[0]) < 3 :
# 	detector = cv2.SimpleBlobDetector(params)
# else : 
# 	detector = cv2.SimpleBlobDetector_create(params)

  # Process video and track objects
while cap.isOpened():
  success, frame = cap.read()
  if not success:
    break
  
  # get updated location of objects in subsequent frames
  success, boxes = multiTracker.update(frame)

  # draw tracked objects
  for i, newbox in enumerate(boxes):
      x1 = int(newbox[0])
      y1 = int(newbox[1])
      x2 = int(newbox[0])+int(newbox[2])
      y2 = int(newbox[1])+int(newbox[3])
      p1 = (x1, y1)
      p2 = (x2, y2)
      cen_x = int((x1+x2)/2)
      cen_y = int((y1+y2)/2)
      #cv2.rectangle(frame, p1, p2, colors[i], 2, 1)
      cv2.circle(frame,(cen_x,cen_y),15,(255,0,255))


      #colored
      dst = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)

      minGray = 255
      new_col,new_row=0,0
      
      for i in range(y1,y2):
          for j in range(x1,x2):
              if(dst[i,j]<minGray):
                minGray=dst[i,j]
                new_col,new_row=i,j
      print(new_col,new_row)
      seed_points = [(new_col,new_row)]  #输入选取的种子像素
      seed_grow_image = regional_growth(y1,y2,x1,x2,frame,dst,seed_points,3)
      #cv2.circle(frame,(new_col,new_row),10,(0,0,255))

      

      # target = frame[y1:y2, x1:x2]
      # #target = frame[int(newbox[1]):int(newbox[1])+int(newbox[3]), int(newbox[0]):int(newbox[0])+int(newbox[2])]
      # cv2.imshow('target',target)
      # #Detect blobs.
      # dst=cv2.cvtColor(target,cv2.COLOR_RGB2GRAY)
      # keypoints = detector.detect(dst)

      # frame = cv2.drawKeypoints(dst,keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
      

  # show frame
  cv2.imshow('MultiTracker', frame)

  #save
  out.write(frame)
  

  # quit on ESC button
  if cv2.waitKey(1) & 0xFF == 27:  # Esc pressed
    break


