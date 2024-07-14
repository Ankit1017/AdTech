from flask import Flask,render_template,request
app = Flask(__name__)
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
    	    return render_template("signup.html", message="Comming Soon")

@app.route("/sign_in", methods=["GET","POST"])
def main3():
	if (request.method == "GET"):
		return render_template("signin.html", message="")
	else:
			return render_template("signin.html",message="Comming Soon")