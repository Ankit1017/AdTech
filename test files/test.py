from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sites.db'
db = SQLAlchemy(app)
from datetime import datetime
from moviepy.editor import VideoFileClip
import random
import string

def generate_secret_string(length=10):
    """Generate a random secret string of a specified length."""
    # Define the characters to choose from
    characters = string.ascii_letters + string.digits + string.punctuation

    # Generate the secret string
    secret_string = ''.join(random.choice(characters) for _ in range(length))

    return secret_string
class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(255))
    ad_name = db.Column(db.String(255))
    category_name = db.Column(db.String(255))
    time_shown = db.Column(db.DateTime, default=datetime.utcnow)
    camera_address = db.Column(db.String(255))
    unique_id = db.Column(db.String(255))

    def __init__(self, company_name, ad_name, category_name, camera_address, unique_id):
        self.company_name = company_name
        self.ad_name = ad_name
        self.category_name = category_name
        self.camera_address = camera_address
        self.unique_id = unique_id

class BarGraphData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(255))
    ad_data = db.Column(db.JSON)

    def __init__(self, company_name, ad_data):
        self.company_name = company_name
        self.ad_data = ad_data

class LineGraphData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(255))
    date_views = db.Column(db.JSON)

    def __init__(self, company_name, date_views):
        self.company_name = company_name
        self.date_views = date_views

class PieGraphData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(255))
    ad_data = db.Column(db.JSON)

    def __init__(self, company_name, ad_data):
        self.company_name = company_name
        self.ad_data = ad_data

class AssociationData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(255))
    cat_data = db.Column(db.JSON)

    def __init__(self, category_name, cat_data):
        self.category_name = category_name
        self.cat_data = cat_data

class ThomsonData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(255))
    cat_data = db.Column(db.JSON)

    def __init__(self, category_name, cat_data):
        self.category_name = category_name
        self.cat_data = cat_data
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    mobile_number = db.Column(db.String(20), unique=True)
    cat_name=db.Column(db.String(255))
    account_balance = db.Column(db.Float, default=0.0)
    file_space_capacity = db.Column(db.Float, default=0.0) 
    file_links = db.Column(db.JSON)
    def __init__(self, username, password, email, mobile_number,cat_name,account_balance=0.0, file_space_capacity=0.0,file_links=None):
        self.username = username
        self.password = password
        self.email = email
        self.mobile_number = mobile_number
        self.cat_name=cat_name
        self.account_balance = account_balance
        self.file_space_capacity = file_space_capacity
        self.file_links = file_links or {}
        
        
class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    video_link = db.Column(db.String(255), nullable=False)
    video_id=db.Column(db.String(255), unique=True)
    name = db.Column(db.String(100), nullable=False)
    length = db.Column(db.Integer, nullable=False)
    uploaded_at = db.Column(db.String(255), nullable=False)
    user = db.Column(db.String(100))

    def __init__(self, video_link, name, user,id,at):
        self.video_link = video_link
        self.name = name
        clip = VideoFileClip(video_link)
        self.length = int(clip.duration)
        self.user = user
        self.video_id=id
        self.uploaded_at=at
        
with app.app_context():
    # for i in os.listdir("static/uploads"):
    #     for j in os.listdir("static/uploads/"+i):
    #         for k in os.listdir("static/uploads/"+i+"/"+j):
    #             db.session.add(Video(video_link="static/uploads/"+i+"/"+j+"/"+k, name=k, user=j,id=generate_secret_string(4),at=datetime.now()))
    #             db.session.commit()
    
    # at=User.query.all()
    # for i in at:
    #     print(i.username)
    import json,os
    with open(r'D:\projects\ads_selector\sampling\sampling result\association.json', 'r') as csvfile:  # Replace with your CSV file name
        csv_reader = json.load(csvfile)
        screen_no=csv_reader
        # print(screen_no)
        k=0
        for i in os.listdir(r"D:\projects\ads_selector\static\uploads"):
            db.session.add(AssociationData(i,screen_no[k]))
            db.session.commit()
            k+=1
            
# with app.app_context():
    
#     users_with_zero_balance = User.query.filter_by(account_balance=0.0).all()

# # Extract cat_name and username from the users with zero balance
#     cat_names = list(set(user.cat_name for user in users_with_zero_balance))
#     usernames = [user.username for user in users_with_zero_balance]

#     print("Cat Names with Zero Account Balance:", cat_names)
#     print("Usernames with Zero Account Balance:", usernames)
#                 at2=ThomsonData.query.filter(ThomsonData.category_name == "beverage").all()
#                 for a in at2:
#                     r3=a.cat_data
#                 print(r3)
# with app.app_context():
#     amount_to_add = 0
#     User.query.filter(User.username=="coca").update({User.account_balance: amount_to_add})
#     db.session.commit()

    # users_with_zero_balance = User.query.filter_by(account_balance=0.0).all()

    # # Create a dictionary to store cat_name and its corresponding usernames
    # cat_username_dict = {}
    # for user in users_with_zero_balance:
    #     if user.cat_name not in cat_username_dict:
    #         cat_username_dict[user.cat_name] = [user.username]
    #     else:
    #         cat_username_dict[user.cat_name].append(user.username)
    # print(cat_username_dict)
    # # Filter cat_names where all associated usernames have account_balance zero
    # unique_cat_names = [cat_name for cat_name, usernames in cat_username_dict.items() if [cl.username for cl in User.query.filter_by(cat_name=cat_name).all()] ==usernames]

    # usernames = [user.username for user in users_with_zero_balance]

    # print("Unique Cat Names with Zero Account Balance:", unique_cat_names)
    # print("Usernames with Zero Account Balance:", usernames)