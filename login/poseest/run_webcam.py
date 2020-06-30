import argparse
import logging
import time

import cv2
import numpy as np

from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh



logger = logging.getLogger('TfPoseEstimator-WebCam')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

fps_time = 0

def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")


if __name__ == '__main__':
    
    '''logger.debug('initialization %s : %s' % (args.model, get_graph_path(args.model)))'''
    w=432
    h=368
    
    e = TfPoseEstimator(get_graph_path('mobilenet_thin'), target_size=(432, 368), trt_bool=False)
    logger.debug('cam read+')
    cam = cv2.VideoCapture(0)
    ret_val, image = cam.read()
    '''logger.info('cam image=%dx%d' % (image.shape[1], image.shape[0]))'''

    while True:
        ret_val, image = cam.read()

        '''logger.debug('image process+')'''
        humans = e.inference(image, resize_to_default=(w > 0 and h > 0), upsample_size=4.0)
        print(humans)
        
        '''logger.debug(humans)'''
        '''logger.debug('postprocess+')'''
        image = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)

        '''logger.debug('show+')'''
        cv2.putText(image,
                    "FPS: %f" % (1.0 / (time.time() - fps_time)),
                    (10, 10),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 255, 0), 2)
        cv2.imshow('tf-pose-estimation result', image)
        fps_time = time.time()
        if cv2.waitKey(1) == 27:
            break
        logger.debug('finished+')

    cv2.destroyAllWindows()
