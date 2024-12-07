from flask import Flask, redirect, url_for, render_template, request, flash
from config import get_db_connection, init_db

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize the database
init_db()

@app.route("/", methods=["POST", "GET"])
def home():
    return render_template("homepage.html")

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']

        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for('register'))
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                         (username, email, password))
            conn.commit()
            conn.close()
            flash("Registration successful!", "success")
            return redirect(url_for('login'))
    return render_template("register.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)


