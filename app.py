from flask import render_template, send_file,request,redirect,url_for
import os, datetime,secrets
from datetime import datetime
from init import app,db
from database_cls import *
import razorpay
from collections import defaultdict
from graph_data_extraxtor import cf
client = razorpay.Client(auth=("rzp_test_uyBf3XXupL0quV", "cJaG9We90tlyBG2b6NDQtgEa"))
def rf(a):
    	return open(a,"r").read()
@app.route("/",methods=["GET"])
def main():
	return render_template("index.html")
@app.route("/about_us",methods=["GET"])
def mainabt():
	return render_template("about-us.html")
@app.route("/contact_us",methods=["GET"])
def mainct():
	return render_template("contact-us.html")
@app.route("/sign_up", methods=["GET","POST"])
def main2():
	if (request.method == "GET"):
		return render_template("signup.html", message="")
	else:
		w = [request.form["username"], request.form["password"], request.form["email"], request.form["name"],request.form["mobile_number"],request.form["category"]]
		data = User.query.filter_by(username=w[0]).first()
		if (data):
			return render_template("signup.html", message="Account already exists")
		else:
			os.mkdir("static/uploads/"+w[5]+"/"+w[0])
			db.session.add(User(username=w[0], password=w[1],email=w[2],mobile_number=w[4],cat_name=w[5]))
			db.session.commit()
			return redirect(url_for("main17", user=w[0],cat=w[5]))
@app.route("/sign_in", methods=["GET","POST"])
def main3():
	if (request.method == "GET"):
		return render_template("signin.html", message="")
	else:
		w = [request.form["username"], request.form["password"],request.form["category"]]
		data=User.query.filter_by(username=w[0], password=w[1],cat_name=w[2]).first()
		if data is not None:
			return redirect(url_for("main17",user=w[0],cat=w[2]))
		else:
			return render_template("signin.html",message="Either you enter Wrong password or no such account present or you have choose wrong category")
@app.route("/logout")
def main19():
    return redirect(url_for("main"))
@app.route("/dashboard/<cat>/<user>", methods=["GET", "POST"])
def main17(user,cat):
    if request.method == 'POST':
        amount=int(request.form.get("amt"))*100
        data = { "amount": amount, "currency": "INR", "receipt": "order_rcptid_11" }
        payment = client.order.create(data=data)
        pdata=[amount, payment["id"]]
        print(pdata[0])
        return render_template("rp.html", pdata=pdata,amt=pdata[0],user=user,cat=cat)
    else:
        data=User.query.filter_by(username=user,cat_name=cat).first()
        name=user
        password=data.password
        balance=data.account_balance
        balance=round(int(balance),4)
        files = []
        space=0
        print("static/uploads/"+cat+"/"+user)
        for i in os.listdir("static/uploads/"+cat+"/"+user+"/"):
            print(i)
            files.append({"name":i,"d_name":i[:20],"size":str(round(os.path.getsize("static/uploads/"+cat+"/"+user+"/"+i)/1024/1024))+" mb"})
            space = space+os.path.getsize("static/uploads/"+cat+"/"+user+"/"+i)/1024/1024
        data.space=space
        print(files)
        return render_template('dashboard.html', name=name, files=files, password=password, username=user, space=round(space), nf=len(files),cat=cat,balance=balance)
@app.route('/success/<cat>/<user>/<amt>', methods=["POST"])
def success(cat,user,amt):
    pid=request.form.get("razorpay_payment_id")
    ordid=request.form.get("razorpay_order_id")
    sign=request.form.get("razorpay_signature")
    print(f"The payment id : {pid}, order id : {ordid} and signature : {sign} and added {amt}")
    params={
    'razorpay_order_id': ordid,
    'razorpay_payment_id': pid,
    'razorpay_signature': sign
    }
    final=client.utility.verify_payment_signature(params)
    if final == True:
        data=User.query.filter_by(username=user,cat_name=cat).first()
        data.account_balance += float(amt) / 100
        db.session.commit()
        return redirect(url_for("main17",user=user,cat=cat))
    return "Something Went Wrong Please Try Again"
@app.route("/upload/<cat>/<user>/file", methods=["POST"])
def main4(user, cat):
    if request.method == "POST":
        pas = User.query.filter_by(username=user, cat_name=cat).first().password
        w = [user, pas, cat]
        data = User.query.filter_by(username=w[0], password=w[1]).first()
        if data is not None:
            file = request.files['files[]']
            if file.filename == '':
                return 'No selected file'
            folder_path = os.path.join("static","uploads", w[2], user)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            file.save(os.path.join(folder_path, file.filename))
            vd = Video(video_link=os.path.join(folder_path, file.filename), name=file.filename, user=w[0], id=str(secrets.token_urlsafe(4)), at=datetime.now())
            db.session.add(vd)
            db.session.commit()
        else:
            print("User data is None, unable to save files.")
        return redirect(url_for("main17", user=w[0], cat=cat))
@app.route("/delete/<cat>/<user>/<name>", methods=["GET"])
def main5(user, name, cat):
    if (request.method == "GET"):
        if (name in os.listdir("static/uploads/"+cat+"/"+user)):
            os.remove("static/uploads/"+cat+"/"+user+"/"+name)
            data=Video.query.filter_by(user=user,name=name).first()
            if data:
                db.session.delete(data)
    return redirect(url_for("main17", user=user,cat=cat))
@app.route("/download/<cat>/<user>/<name>", methods=["GET"])
def main15(user, name,cat):
	if (request.method == "GET"):
		if (name in os.listdir("static/uploads/"+cat+"/"+user)):
			return send_file("static/uploads/"+cat+"/"+user+"/"+name)
	return redirect(url_for("main17", user=user,cat=cat))
@app.errorhandler(404)
def main10(e):
	return render_template("404.html")
@app.route("/view/<cat>/<user>")
def main16(user,cat):
    logs = Log.query.filter_by(category_name=cat,company_name=user).all()
    logs_data = [{
        'name': log.ad_name,
        'location': log.camera_address,
        'timeShown': str(log.time_shown.strftime('%Y-%m-%d %H:%M:%S'))
    } for log in logs]
    return render_template('view.html', username=user,name=user,cat=cat,log=logs_data)
@app.route("/view/<cat>/<user>/<name>")
def main21(user,name,cat):
    logs = Log.query.filter(Log.company_name==user,Log.category_name==cat,Log.ad_name==name).all()
    logs_data = [{
        'name': log.ad_name,
        'location': log.camera_address,
        'timeShown': str(log.time_shown.strftime('%Y-%m-%d %H:%M:%S'))
    } for log in logs]
    return render_template('view_ad.html', username=user,name=user,ad_name=name,cat=cat,log=logs_data)
@app.route("/stat/<cat>/<user>")
def main18(user,cat):
    ad_runs_data = {}
    ad_runs_data1 = {}
    ad_runs_data2 = {}
    views_by_date = defaultdict(int)
    datasets = []
    cf(user,cat,ad_runs_data,ad_runs_data1,ad_runs_data2,views_by_date,datasets)
    return render_template('test.html', username=user,name=user,cat=cat,dtw=ad_runs_data,dtm=ad_runs_data1,dty=ad_runs_data2,vd1=views_by_date,dataset=datasets)
@app.route("/stat/<cat>/<user>/<name>")
def main20(user,name,cat):
    ad_runs_data = {}
    ad_runs_data1 = {}
    ad_runs_data2 = {}
    views_by_date = defaultdict(int)
    datasets = []
    cf(user,cat,ad_runs_data,ad_runs_data1,ad_runs_data2,views_by_date,datasets,name)
    return render_template('stat_ad.html', username=user,name=user,ad_name=name,cat=cat,dtw=ad_runs_data,dtm=ad_runs_data1,dty=ad_runs_data2,vd1=views_by_date,dataset=datasets)
if __name__ == '__main__':
    app.run(port=3000)