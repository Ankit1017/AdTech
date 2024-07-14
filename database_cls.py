from init import db,app
from datetime import datetime
from moviepy.editor import VideoFileClip
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
        
