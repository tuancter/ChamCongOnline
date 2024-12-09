from flask import Flask, redirect, url_for, render_template, request, flash, get_flashed_messages, send_from_directory, session
from config import get_db_connection, init_db
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'chamcongdb_key'

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
        role = request.form.get('role', 'user')

        if password != confirm_password:
            flash("Mật khẩu không khớp!", "danger")
            return redirect(url_for('register'))
        else:
            try:
                conn = get_db_connection()
                conn.execute('INSERT INTO accounts (username, email, password, role) VALUES (?, ?, ?, ?)',
                             (username, email, password, role))
                conn.commit()
                conn.close()
                flash("Đăng ký thành công!", "success")
                return redirect(url_for('login'))
            except Exception as e:
                logging.error(f"Error inserting into accounts: {e}")
                flash("Đã xảy ra lỗi khi đăng ký!", "danger")
                return redirect(url_for('register'))
    return render_template("register.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        
        try:
            conn = get_db_connection()
            user = conn.execute('SELECT * FROM accounts WHERE username = ? AND password = ?', (username, password)).fetchone()
            conn.close()
            
            if user:
                session['user_id'] = user['id_account']
                flash("Đăng nhập thành công!", "success")
                if user['role'] == 'admin':
                    return redirect(url_for('admin'))
                else:
                    return redirect(url_for('user'))
            else:
                flash("Sai thông tin đăng nhập!", "danger")
                return redirect(url_for('login'))
        except Exception as e:
            logging.error(f"Error querying accounts: {e}")
            flash("Đã xảy ra lỗi khi đăng nhập!", "danger")
            return redirect(url_for('login'))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop('user_id', None)
    flash("Đăng xuất thành công.", "success")
    return redirect(url_for('login'))

@app.route("/set_flash")
def set_flash():
    flash("This is a flash message!", "info")
    return redirect(url_for('show_flash'))

@app.route("/show_flash")
def show_flash():
    return render_template("show_flash.html")

@app.route("/user")
def user():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    conn = get_db_connection()
    user_info = conn.execute('SELECT * FROM users WHERE id_account = ?', (user_id,)).fetchone()
    account_info = conn.execute('SELECT * FROM accounts WHERE id_account = ?', (user_id,)).fetchone()
    conn.close()

    return render_template("user.html", user_info=user_info, account_info=account_info)

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/profile", methods=["GET", "POST"])
def profile():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    conn = get_db_connection()
    user_info = conn.execute('SELECT * FROM users WHERE id_account = ?', (user_id,)).fetchone()

    if request.method == "POST":
        name = request.form['name']
        dateOfBirth = request.form['dateOfBirth']
        address = request.form['address']
        phone_number = request.form['phone_number']
        email = request.form['email']
        position = request.form['position']
        salary = request.form['salary']

        try:
            if user_info:
                conn.execute('UPDATE users SET name = ?, dateOfBirth = ?, address = ?, phone_number = ?, email = ?, position = ?, salary = ? WHERE id_account = ?',
                             (name, dateOfBirth, address, phone_number, email, position, salary, user_id))
            else:
                conn.execute('INSERT INTO users (id_account, name, dateOfBirth, address, phone_number, email, position, salary) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                             (user_id, name, dateOfBirth, address, phone_number, email, position, salary))
            conn.commit()
            flash("Thông tin đã được cập nhật.", "success")
        except Exception as e:
            logging.error(f"Error updating/inserting users: {e}")
            flash("Đã xảy ra lỗi khi cập nhật thông tin!", "danger")
        finally:
            conn.close()
        return redirect(url_for('profile'))

    conn.close()
    return render_template("profile.html", user_info=user_info)
    
@app.route('/images/<path:filename>')
def static_files(filename):
    return send_from_directory('images', filename)

if __name__ == "__main__":
    app.run(debug=True)


