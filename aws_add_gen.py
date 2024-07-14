import cv2
from moviepy.editor import VideoFileClip
from random import choices
import time
from model import fun
from flask import render_template
import random
from init import app
import boto3
from boto3.dynamodb.conditions import Attr
from datetime import datetime
from decimal import Decimal
import ast
from over_fun import *
session = boto3.session.Session(profile_name='Ankit')
dc=session.client('dynamodb')
cap2=cv2.VideoCapture('rt1.mp4')
video_folder_path='https://hatchedadtech.s3.ap-south-1.amazonaws.com/uploads'
def generate_frames_dual(f1,f2):
    while True:
        # ret,frame = cap.read()
        # ret,frame1 = cap1.read()
        ret,frame2 = cap2.read()
        # c1=fun(frame)
        # c2=fun(frame1)
        c3=fun(frame2)
        if(c3>0):
            bucket_name = 'hatchedadtech'
            prefix = 'uploads/'
            items = list_folders_in_bucket(bucket_name, prefix)
            with app.app_context():
                db=session.resource('dynamodb')
                user_table = db.Table('User')
                response = user_table.scan(
                    FilterExpression=Attr('account_balance').eq(Decimal(0.0))
                )
                users_with_zero_balance = response['Items']
                association_table = db.Table('AssociationData')
                response = association_table.scan(
                    FilterExpression=Attr('category_name').eq(f1)
                )
                item = response['Items'][0]
                r1 = item['cat_data']
                response = association_table.scan(
                    FilterExpression=Attr('category_name').eq(f2)
                )
                item = response['Items'][0]
                r2 = item['cat_data']
                cat_username_dict = {}
                for user in users_with_zero_balance:
                    if user['cat_name'] not in cat_username_dict:
                        cat_username_dict[user['cat_name']] = [user['username']]
                    else:
                        cat_username_dict[user['cat_name']].append(user['username'])
                cat_names = [cat_name for cat_name, usernames in cat_username_dict.items() if [cl['username'] for cl in user_table.scan(FilterExpression=Attr('cat_name').eq(cat_name))['Items']] ==usernames]
            usernames = [user['username'] for user in users_with_zero_balance]
            quantities=r1
            quantities1=r2
            num_to_pick = 1 
            print(type(items))
            print(type(quantities))
            print(num_to_pick)
            print(type(cat_names))
            p=item_picker_avoider(items, ast.literal_eval(quantities), num_to_pick,cat_names)
            p2=item_picker_avoider(items,ast.literal_eval(quantities1), num_to_pick,cat_names)
            p=random.choice([p,p2])
            print(p)
            companies=list_folders_in_bucket(bucket_name,"uploads/"+p[0]+"/")
            print(companies)
            with app.app_context():
                thomson_table = db.Table('ThomsonData')
                response = thomson_table.scan(
                    FilterExpression=Attr('category_name').eq(p[0])
                )
                item = response['Items'][0]
                r3 = item['cat_data']
            q=item_picker_avoider(companies,ast.literal_eval(r3),1,usernames)
            avai=list_objects_in_bucket(bucket_name,"uploads/"+p[0]+"/"+q[0]+"/")
            r=item_picker(avai,[1 for i in range(len(avai))],1)
            print(r)
            s=video_folder_path+"/"+str(p[0])+"/"+str(q[0])+"/"+r[0]
            bucket_name = "hatchedadtech"
            object_key = "uploads/"+str(p[0])+"/"+str(q[0])+"/"+r[0]
            expiration_time = 3600 

            presigned_url = generate_presigned_url(bucket_name, object_key, expiration_time)
            print(s)
            s=presigned_url
            print(s)
            with app.app_context():
                yield render_template('display_ads.html',url_link=s)
            clip = VideoFileClip(s)
            print(clip.duration)
            with app.app_context():
                db=session.resource('dynamodb')
                table = db.Table('Log')
                response = table.scan(Select='COUNT')
                item_count = response['Count']
                data = {
                    'id': item_count+1,
                    'company_name': q[0],
                    'ad_name': r[0],
                    'category_name': p[0],
                    'time_shown': datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
                    'camera_address': 'null',
                    'unique_id': generate_secret_code()
                }
                table.put_item(Item=data)
                table = db.Table('User')
                response = table.scan(
                    FilterExpression=Attr('username').eq(q[0])&  Attr('cat_name').eq(p[0])
                )
                id=response['Items'][0]['id']
                deduction_amount = (Decimal(10) / Decimal(100)) * Decimal(clip.duration)
                response = table.update_item(
                    Key={
                        'id': id
                    },
                    UpdateExpression='SET account_balance = account_balance - :val',
                    ExpressionAttributeValues={
                        ':val': deduction_amount
                    },
                    ReturnValues='UPDATED_NEW'
                )
            time.sleep(clip.duration)
            
def generate_frames_single(f1):
    while True:
        # ret,frame = cap.read()
        # ret,frame1 = cap1.read()
        ret,frame2 = cap2.read()
        # c1=fun(frame)
        # c2=fun(frame1)
        c3=fun(frame2)
        if(c3>0):
            bucket_name = 'hatchedadtech'
            prefix = 'uploads/'
            items = list_folders_in_bucket(bucket_name, prefix)
            with app.app_context():
                db=session.resource('dynamodb')
                user_table = db.Table('User')
                response = user_table.scan(
                    FilterExpression=Attr('account_balance').eq(Decimal(0.0))
                )
                users_with_zero_balance = response['Items']
                association_table = db.Table('AssociationData')
                response = association_table.scan(
                    FilterExpression=Attr('category_name').eq(f1)
                )
                item = response['Items'][0]
                r1 = item['cat_data']
                cat_username_dict = {}
                for user in users_with_zero_balance:
                    if user['cat_name'] not in cat_username_dict:
                        cat_username_dict[user['cat_name']] = [user['username']]
                    else:
                        cat_username_dict[user['cat_name']].append(user['username'])
                cat_names = [cat_name for cat_name, usernames in cat_username_dict.items() if [cl['username'] for cl in user_table.scan(FilterExpression=Attr('cat_name').eq(cat_name))['Items']] ==usernames]
            usernames = [user['username'] for user in users_with_zero_balance]
            quantities=r1
            num_to_pick = 1 
            print(type(items))
            print(type(quantities))
            print(num_to_pick)
            print(type(cat_names))
            p=item_picker_avoider(items, ast.literal_eval(quantities), num_to_pick,cat_names)
            print(p)
            companies=list_folders_in_bucket(bucket_name,"uploads/"+p[0]+"/")
            print(companies)
            with app.app_context():
                thomson_table = db.Table('ThomsonData')
                response = thomson_table.scan(
                    FilterExpression=Attr('category_name').eq(p[0])
                )
                item = response['Items'][0]
                r3 = item['cat_data']
            q=item_picker_avoider(companies,ast.literal_eval(r3),1,usernames)
            avai=list_objects_in_bucket(bucket_name,"uploads/"+p[0]+"/"+q[0]+"/")
            r=item_picker(avai,[1 for i in range(len(avai))],1)
            print(r)
            s=video_folder_path+"/"+str(p[0])+"/"+str(q[0])+"/"+r[0]
            bucket_name = "hatchedadtech"
            object_key = "uploads/"+str(p[0])+"/"+str(q[0])+"/"+r[0]
            expiration_time = 3600 

            presigned_url = generate_presigned_url(bucket_name, object_key, expiration_time)
            print(s)
            s=presigned_url
            print(s)
            with app.app_context():
                yield render_template('display_ads.html',url_link=s)
            clip = VideoFileClip(s)
            print(clip.duration)
            with app.app_context():
                db=session.resource('dynamodb')
                table = db.Table('Log')
                response = table.scan(Select='COUNT')
                item_count = response['Count']
                data = {
                    'id': item_count+1,
                    'company_name': q[0],
                    'ad_name': r[0],
                    'category_name': p[0],
                    'time_shown': datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
                    'camera_address': 'null',
                    'unique_id': generate_secret_code()
                }
                table.put_item(Item=data)
                table = db.Table('User')
                response = table.scan(
                    FilterExpression=Attr('username').eq(q[0])&  Attr('cat_name').eq(p[0])
                )
                id=response['Items'][0]['id']
                deduction_amount = (Decimal(10) / Decimal(100)) * Decimal(clip.duration)
                response = table.update_item(
                    Key={
                        'id': id
                    },
                    UpdateExpression='SET account_balance = account_balance - :val',
                    ExpressionAttributeValues={
                        ':val': deduction_amount
                    },
                    ReturnValues='UPDATED_NEW'
                )
            time.sleep(clip.duration)
