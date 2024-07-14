import os,cv2
from moviepy.editor import VideoFileClip
from company_sector import selector,item_picker
from associations import screen_no
import time
from model import fun
from flask import Flask, render_template, Response,stream_with_context

app = Flask(__name__)
# cap = cv2.VideoCapture('rt1.mp4')
# cap1=cv2.VideoCapture("rt.mp4")
cap2=cv2.VideoCapture('rt1.mp4')



video_folder_path="static/uploads"

app.config['UPLOAD_FOLDER']=video_folder_path
app.secret_key="abbb"






def generate_frames():
    while True:
        # ret,frame = cap.read()
        # ret,frame1 = cap1.read()
        ret,frame2 = cap2.read()
        # c1=fun(frame)
        # c2=fun(frame1)
        c3=fun(frame2)
        if(c3>0):
            items = os.listdir(video_folder_path)
            quantities = screen_no[5]
            num_to_pick = 1 
            p=item_picker(items, quantities, num_to_pick)
            print(p)
            companies=os.listdir(video_folder_path+"/"+p[0])
            print(companies)
            q=item_picker(companies,[1 for i in range(len(companies))],1)       #thomson
            avai=os.listdir(video_folder_path+"/"+p[0]+"/"+q[0])
            r=item_picker(avai,[1 for i in range(len(avai))],1)
            print(r)
            s="./"+video_folder_path+"/"+str(p[0])+"/"+str(q[0])+"/"+r[0]
            s1=video_folder_path+"/"+str(p[0])+"/"+str(q[0])+"/"+r[0]
            print(s)
            with app.app_context():
                yield render_template('display_ads.html',url_link=s)
            clip = VideoFileClip(s1)
            print(clip.duration)
            time.sleep(clip.duration)
            
@app.route('/')
def add_show():
    return Response(stream_with_context(generate_frames()))
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5004)