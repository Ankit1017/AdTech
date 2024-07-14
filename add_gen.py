import os,cv2
from moviepy.editor import VideoFileClip
from random import choices
import time
from model import fun
from flask import render_template
import random,secrets,string
from init import app,db
from database_cls import *
cap2=cv2.VideoCapture('rt1.mp4')
video_folder_path="static/uploads"
def item_picker(items, quantities, num_to_pick):
    return choices(items, weights=quantities, k=num_to_pick)
def item_picker_avoider(items, quantities, num_to_pick, elements_to_avoid):
    filtered_items = [item for item in items if item not in elements_to_avoid]
    filtered_quantities = [quantities[idx] for idx, item in enumerate(items) if item not in elements_to_avoid]
    if not filtered_items:
        return []
    chosen_items = choices(filtered_items, weights=filtered_quantities, k=num_to_pick)
    return chosen_items
def generate_secret_code(length=12):
    alphabet = string.ascii_letters + string.digits  # You can include more characters if needed
    secret_code = ''.join(secrets.choice(alphabet) for _ in range(length))
    return secret_code
def generate_frames_dual(f1,f2):
    while True:
        # ret,frame = cap.read()
        # ret,frame1 = cap1.read()
        ret,frame2 = cap2.read()
        # c1=fun(frame)
        # c2=fun(frame1)
        c3=fun(frame2)
        if(c3>0):
            items = os.listdir(video_folder_path)
            with app.app_context():
                users_with_zero_balance = User.query.filter_by(account_balance=0.0).all()
                at=AssociationData.query.filter(AssociationData.category_name == f1).all()
                for i in at:
                    r1=i.cat_data
                at1=AssociationData.query.filter(AssociationData.category_name == f2).all()
                for i in at1:
                    r2=i.cat_data
                cat_username_dict = {}
                for user in users_with_zero_balance:
                    if user.cat_name not in cat_username_dict:
                        cat_username_dict[user.cat_name] = [user.username]
                    else:
                        cat_username_dict[user.cat_name].append(user.username)
                cat_names = [cat_name for cat_name, usernames in cat_username_dict.items() if [cl.username for cl in User.query.filter_by(cat_name=cat_name).all()] ==usernames]
            usernames = [user.username for user in users_with_zero_balance]
            quantities=r1
            quantities1=r2
            num_to_pick = 1 
            p=item_picker_avoider(items, quantities, num_to_pick,cat_names)
            p2=item_picker_avoider(items, quantities1, num_to_pick,cat_names)
            p=random.choice([p,p2])
            print(p)
            companies=os.listdir(video_folder_path+"/"+p[0])
            print(companies)
            with app.app_context():
                at2=ThomsonData.query.filter(ThomsonData.category_name == p[0]).all()
                for a in at2:
                    r3=a.cat_data
            q=item_picker_avoider(companies,r3,1,usernames)       #thomson
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
            with app.app_context():
                lg=Log(
                    company_name=q[0],
                    ad_name=r[0],
                    category_name=p[0],
                    camera_address="null",
                    unique_id=generate_secret_code()
                )
                db.session.add(lg)
                db.session.commit()
                data=User.query.filter_by(username=q[0],cat_name=p[0]).first()
                data.account_balance -= (float(10) / 100) * float(clip.duration)
                db.session.commit()
            time.sleep(clip.duration)
def generate_frames_single(f1):
    while True:
        # ret,frame = cap.read()
        # ret,frame1 = cap1.read()
        ret,frame2 = cap2.read()
        # c1=fun(frame)
        # c2=fun(frame1)
        c3=fun(frame2)
        if c3>0:
            items = os.listdir(video_folder_path)
            with app.app_context():
                users_with_zero_balance = User.query.filter_by(account_balance=0.0).all()
                at=AssociationData.query.filter(AssociationData.category_name == f1).all()
                for i in at:
                    r1=i.cat_dat
                cat_username_dict = {}
                for user in users_with_zero_balance:
                    if user.cat_name not in cat_username_dict:
                        cat_username_dict[user.cat_name] = [user.username]
                    else:
                        cat_username_dict[user.cat_name].append(user.username)
                cat_names = [cat_name for cat_name, usernames in cat_username_dict.items() if [cl.username for cl in User.query.filter_by(cat_name=cat_name).all()] ==usernames]
            usernames = [user.username for user in users_with_zero_balance]
            quantities=r1
            num_to_pick = 1 
            p=item_picker_avoider(items, quantities, num_to_pick,cat_names)
            print(p)
            companies=os.listdir(video_folder_path+"/"+p[0])
            print(companies)
            with app.app_context():
                at=ThomsonData.query.filter(ThomsonData.category_name == p[0]).all()
                for a in at:
                    r1=a.cat_data
            q=item_picker_avoider(companies,r1,1,usernames)
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
            with app.app_context():
                lg=Log(
                    company_name=q[0],
                    ad_name=r[0],
                    category_name=p[0],
                    camera_address="null",
                    unique_id=generate_secret_code()
                )
                db.session.add(lg)
                db.session.commit()
                data=User.query.filter_by(username=q[0],cat_name=p[0]).first()
                data.account_balance -= (float(10) / 100)  * float(clip.duration)
                db.session.commit()
            time.sleep(clip.duration)
