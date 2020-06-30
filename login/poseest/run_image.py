import argparse
import logging
import time
import array
import math

import cv2
import numpy as np

from statistics import mean

from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh


logger = logging.getLogger('TfPoseEstimator-IMAGE')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

fps_time = 0

time_start=time.time()


def compare(live_x,live_y,orig_x,orig_y):
    arr=[0]
    arr1=[0]
    arr2=[0]
    arr3=[0]

    points_dict={0:[0,1],1:[1,2],2:[2,3],3:[3,4],4:[1,5],5:[5,6],6:[6,7],7:[1,8],8:[8,9],9:[9,10],10:[1,11],
            11:[11,12],12:[12,13],13:[0,15],14:[15,17],15:[0,14],16:[14,16]}

    i = 0
    while i < 17:
        x1=live_x[points_dict[i][0]]
        x2=live_x[points_dict[i][1]]

        y1=live_y[points_dict[i][0]]
        y2=live_y[points_dict[i][1]]

        if x1 != -999 and y1 != -999 and x2 != -999 and y2 != -999 :
            arr.append(x1-x2)
            arr1.append(y1-y2)

        else :
            arr.append(0)
            arr1.append(0)
        i += 1

    arr.pop(0)
    arr1.pop(0)
#    print('\n\nLIVE')
 #   print(arr)
 #   print(arr1)

    i = 0
    while i < 17:
        x1=orig_x[points_dict[i][0]]
        x2=orig_x[points_dict[i][1]]

        y1=orig_y[points_dict[i][0]]
        y2=orig_y[points_dict[i][1]]

        if x1 != -999 and y1 != -999 and x2 != -999 and y2 != -999 :
            arr2.append(x1-x2)
            arr3.append(y1-y2)

        else :
            arr2.append(0)
            arr3.append(0)
        i += 1

    arr2.pop(0)
    arr3.pop(0)
 #   print('\nORIGINAL')
 #   print(arr2)    
 #   print(arr3)
 #   print('\n')

    arr4=[0]
    for a, b, c, d in zip(arr, arr1, arr2, arr3):
    # print(a, b, c, d)
    # print('\n')
    # print((a*c)+(b*d))
    # print(math.sqrt((a*a)+(b*b))*math.sqrt((c*c)+(d*d)))
        if((a == 0 and b == 0) or (c == 0 and d == 0)):
            arr4.append(0)
        else :
            arr4.append(((a*c)+(b*d))/(math.sqrt((a*a)+(b*b))*math.sqrt((c*c)+(d*d))))

    arr4.pop(0)
  #  print(arr4)
 #   print('\n')
    
    average=mean(arr4)
    print("\n\n\nACCURACY =", 100*round(average, 2))
    print("\n\n")


def form_arr(dict1):
    arr=[]
    i=0
    j=0
    while i<18:
        if i in dict1.keys():
            arr.append(dict1[i])
        else:
            arr.append(-999)
        i=i+1
    return arr
        



if __name__ == '__main__':
    
    w=432
    h=368
    live_x_dict={}
    live_y_dict={}
    live_x_arr=[]
    live_y_arr=[]
    orig_x_dict={}
    orig_y_dict={}
    orig_x_arr=[]
    orig_y_arr=[]

    
    
    e = TfPoseEstimator(get_graph_path('mobilenet_thin'), target_size=(432, 368), trt_bool=False)
    logger.debug('Image read 1 +')
   
    
    
    ##############################################  LIVE ########################################

    image1=cv2.imread('INPUTS/input1.jpg')
    humans1 = e.inference(image1, resize_to_default=(w > 0 and h > 0), upsample_size=4.0)

    for human in humans1:
        dict=human.body_parts
        for k,v in dict.items():
            live_x_dict[v.part_idx]=round(v.x,2)
            live_y_dict[v.part_idx]=round(v.y,2)
                

    live_x_arr=form_arr(live_x_dict)
    live_y_arr=form_arr(live_y_dict)

    print('\n\n******XXXXXXXX LIVE X ARR XXXXXXXXXX************') 
    print(live_x_arr)
    print('******YYYYYYYY LIVE Y ARR YYYYYYYYYY************') 
    print(live_y_arr)

    ############################################ ORIGINAL #############################################
    
    image2=cv2.imread('INPUTS/input2.jpg')
    humans2 = e.inference(image2, resize_to_default=(w > 0 and h > 0), upsample_size=4.0)

    for human in humans2:
        dict=human.body_parts
        for k,v in dict.items():
            orig_x_dict[v.part_idx]=round(v.x,2)
            orig_y_dict[v.part_idx]=round(v.y,2)
        

    orig_x_arr=form_arr(orig_x_dict)
    orig_y_arr=form_arr(orig_y_dict)

    print('\n\n******XXXXXXXX ORIG X ARR XXXXXXXXXX************') 
    print(orig_x_arr)
    print('******YYYYYYYY ORIG Y ARR YYYYYYYYYY************') 
    print(orig_y_arr)
    print('\n\n')

    ##########################################################################################


    compare(live_x_arr,live_y_arr,orig_x_arr,orig_y_arr)

    image1 = TfPoseEstimator.draw_humans(image1, humans1, imgcopy=False)
    cv2.putText(image1,
                    "FPS: %f" % (1.0 / (time.time() - fps_time)),
                    (10, 10),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 255, 0), 2)
    name = 'OUTPUTS/outpu1.jpg'
    
    cv2.imwrite(name, image1)


    image2 = TfPoseEstimator.draw_humans(image2, humans2, imgcopy=False)
    cv2.putText(image2,
                    "FPS: %f" % (1.0 / (time.time() - fps_time)),
                    (10, 10),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 255, 0), 2)
    name = 'OUTPUTS/outpu2.jpg'
    
    cv2.imwrite(name, image2)





    fps_time = time.time()
        


time_end=time.time()
print('Time to execute:') 
print(time_end-time_start)
print(' secs')

cv2.destroyAllWindows()
