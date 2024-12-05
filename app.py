from flask import Flask
from flask import redirect, url_for, render_template, request

app = Flask(__name__)

@app.route("/", methods = ["POST", "GET"])
def home():
    return render_template("homepage.html")

@app.route("/submit", methods = ["POST", "GET"])
def submit():
    if request.method == "POST":
        user_name = request.form["name"]
        user_email = request.form["email"]
        user_phone = request.form["phone"]
        return render_template("homepage.html", name=user_name, email=user_email, phone=user_phone)
    else:
        return render_template("homepage.html")

if __name__ == "__main__":
    app.run(debug=True)


