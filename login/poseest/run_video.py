import argparse
import logging
import time
import array
import math

import cv2
import numpy as np
from statistics import mean

from login.poseest.tf_pose.estimator import TfPoseEstimator
from login.poseest.tf_pose.networks import get_graph_path, model_wh




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
    return 100*average
    


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

def pose(live_input,original_input):
    logger = logging.getLogger('TfPoseEstimator-VIDEO')
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    fps_time = 0

    time_start = time.time()

    v_accuracy = [0]

    w = 432
    h = 368
    live_x_dict = {}
    live_y_dict = {}
    live_x_arr = []
    live_y_arr = []
    orig_x_dict = {}
    orig_y_dict = {}
    orig_x_arr = []
    orig_y_arr = []
    img_array = []

    e = TfPoseEstimator(get_graph_path('mobilenet_thin'), target_size=(432, 368), trt_bool=False)
    logger.debug('Video read+')
    str1 = 'C:/Users/LENOVO IP 510/Desktop/BE_PROJECT/pose/login/poseest/INPUTS/Aadarsh.mp4'
    str2 = 'C:/Users/LENOVO IP 510/Desktop/BE_PROJECT/pose/login/poseest/INPUTS/Aadarsh.mp4'
    cap1 = cv2.VideoCapture(live_input)
    print("1234")
    cap2 = cv2.VideoCapture(original_input)
    print("1234")

    length = int(cap1.get(cv2.CAP_PROP_FRAME_COUNT))
    ret1, image1 = cap1.read()
    ret2, image2 = cap2.read()

    h1 = image1.shape[0]
    h2 = image2.shape[0]
    w1 = image1.shape[1]
    w2 = image2.shape[1]

    str3 = 'C:/Users/LENOVO IP 510/Desktop/BE_PROJECT/AAAK/login/static/inputvideo/output.mp4'

    no = 1;
    while (no < length - 1):
        print('Comparing frame ', no)
        no = no + 1
        ret1, image1 = cap1.read()
        ret2, image2 = cap2.read()

        ##############################################  LIVE ########################################

        humans1 = e.inference(image1, resize_to_default=(w > 0 and h > 0), upsample_size=4.0)

        for human in humans1:
            dict = human.body_parts
            for k, v in dict.items():
                live_x_dict[v.part_idx] = v.x
                live_y_dict[v.part_idx] = v.y

        live_x_arr = form_arr(live_x_dict)
        live_y_arr = form_arr(live_y_dict)

        ############################################ ORIGINAL #############################################

        humans2 = e.inference(image2, resize_to_default=(w > 0 and h > 0), upsample_size=4.0)

        for human in humans2:
            dict = human.body_parts
            for k, v in dict.items():
                orig_x_dict[v.part_idx] = v.x
                orig_y_dict[v.part_idx] = v.y

        orig_x_arr = form_arr(orig_x_dict)
        orig_y_arr = form_arr(orig_y_dict)

        ##########################################################################################
        v_accuracy.append(compare(live_x_arr, live_y_arr, orig_x_arr, orig_y_arr))

        image1 = TfPoseEstimator.draw_humans(image1, humans1, imgcopy=False)
        image2 = TfPoseEstimator.draw_humans(image2, humans2, imgcopy=False)


        dst = np.concatenate((image1, image2), axis=1)
        dim = (800, 400)
        # resize image
        dst = cv2.resize(dst, dim, interpolation=cv2.INTER_AREA)

        img_array.append(dst)
        height, width, layers = dst.shape
        size = (width, height)

    print("\n\nAccuracy :", mean(v_accuracy))
    print("\n\n")
    time_end = time.time()
    print('Time to execute:')
    print(time_end - time_start)
    print(' secs')

    out = cv2.VideoWriter(str3, cv2.VideoWriter_fourcc(*'H264'), 24, size)
    for i in range(len(img_array)):
        out.write(img_array[i])

    out.release()
    cv2.destroyAllWindows()
    return v_accuracy

if __name__ == '__main__':
	print("")
