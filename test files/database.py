from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# Define the Log model
class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(255))
    ad_name = db.Column(db.String(255))
    category_name = db.Column(db.String(255))
    time_shown = db.Column(db.DateTime, default=datetime.utcnow)
    camera_address = db.Column(db.String(255))
    unique_id = db.Column(db.String(255))


class BarGraphData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(255))
    ad_data = db.Column(db.JSON)  # Using JSON field for ad data {ad1: {monday: views, tuesday: views, ...}}
    
    
class LineGraphData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(255))
    date_views = db.Column(db.JSON)  # Using JSON field for date views {date1: views, date2: views, ...}

class PieGraphData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(255))
    ad_data = db.Column(db.JSON)  # Using JSON field for ad data {ad1: views/impressions, ad2: views/impressions, ...}
    
    
    




# Create the table
with app.app_context():
    db.create_all()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
# import psycopg2
# from psycopg2 import sql
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime

# app = Flask(__name__)

# # Configure the PostgreSQL database
# db_params = {
#     'host': 'your_postgresql_host',
#     'port': 'your_postgresql_port',
#     'database': 'your_postgresql_database',
#     'user': 'your_postgresql_username',
#     'password': 'your_postgresql_password'
# }

# # Establish a connection
# conn = psycopg2.connect(**db_params)
# conn.autocommit = True  # Ensure autocommit is set for creating database and tables
# cursor = conn.cursor()

# # Create the database
# cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier('your_postgresql_database')))

# # Close the cursor and connection
# cursor.close()
# conn.close()

# # Switch to the PostgreSQL database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://your_postgresql_username:your_postgresql_password@your_postgresql_host:your_postgresql_port/your_postgresql_database'
# db = SQLAlchemy(app)

# # Define the Log model
# class Log(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     company_name = db.Column(db.String(255))
#     ad_name = db.Column(db.String(255))
#     category_name = db.Column(db.String(255))
#     time_shown = db.Column(db.DateTime, default=datetime.utcnow)
#     camera_address = db.Column(db.String(255))
#     unique_id = db.Column(db.String(255))

# # Create the table
# with app.app_context():
#     db.create_all()

# if __name__ == '__main__':
#     app.run(debug=True)
