import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import cv2

model = hub.load('https://tfhub.dev/google/movenet/multipose/lightning/1')
movenet = model.signatures['serving_default']
def draw_keypoints(frame, keypoints, confidence_threshold):
    y, x, c = frame.shape
    shaped = np.squeeze(np.multiply(keypoints, [y,x,1]))
    
    for kp in shaped:
        ky, kx, kp_conf = kp
        if kp_conf > confidence_threshold:
            cv2.circle(frame, (int(kx), int(ky)), 6, (0,255,0), -1)
def draw_connections(frame, keypoints, edges, confidence_threshold):
    y, x, c = frame.shape
    shaped = np.squeeze(np.multiply(keypoints, [y,x,1]))
    a=0
    for edge, color in edges.items():
        p1, p2 = edge
        y1, x1, c1 = shaped[p1]
        y2, x2, c2 = shaped[p2]
        
        if (c1 > confidence_threshold) & (c2 > confidence_threshold):  
            a=1
            cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0,0,255), 4)
    return a 
EDGES = {
    (0, 1): 'm',
    (0, 2): 'c',
    (1, 3): 'm',
    (2, 4): 'c',
    (0, 5): 'm',
    (0, 6): 'c',
    (5, 7): 'm',
    (7, 9): 'm',
    (6, 8): 'c',
    (8, 10): 'c',
    (5, 6): 'y',
    (5, 11): 'm',
    (6, 12): 'c',
    (11, 12): 'y',
    (11, 13): 'm',
    (13, 15): 'm',
    (12, 14): 'c',
    (14, 16): 'c'
}  
def loop_through_people(frame, keypoints_with_scores, edges, confidence_threshold):
    p=0
    for person in keypoints_with_scores:
        p+=draw_connections(frame, person, edges, confidence_threshold)
        draw_keypoints(frame, person, confidence_threshold)
    return p    
def fun(frame):
    img = frame.copy()
    img = tf.image.resize_with_pad(tf.expand_dims(img, axis=0), 480,864)
    input_img = tf.cast(img, dtype=tf.int32)
    
    # Detection section
    results = movenet(input_img)
    keypoints_with_scores = results['output_0'].numpy()[:,:,:51].reshape((6,17,3))
    
    # Render keypoints 
    
    p=loop_through_people(frame, keypoints_with_scores, EDGES, 0.3)
    print(p)
    return p


#log file:
# a1= company name
# a2= ad name
# a3= category name
# a4= time shown
# a5= camera address
# a6= unique id 


# bar graph data:
# b1= company name
# b2= { ad1:{monday:total view,tuesday:total views...}}

# line graph data:
# c1= company name
# c2= [date:total views]last 7dates counts


# pie graph data:
# d1 = company name
# d2 = {ad1:views/impressions}all ads
