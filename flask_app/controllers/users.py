from flask_app import app
from flask import render_template, request, redirect, session
from flask_bcrypt import Bcrypt 
bcrypt = Bcrypt(app)
from flask import flash
from flask_app.models.user import User
from flask_app.models.alarm import Alarm
from flask_app.models.inquiry import Inquiry

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/alarms')
    return render_template("index.html")

@app.route("/alarms")
def dashboard():
    if 'user_id' not in session:
        return render_template("dashboard.html")
    data = {
        "id": session['user_id']
    }
    return render_template("dashboard.html", user = User.get_one(data), alarms = Alarm.get_all_with_user(data))

@app.route("/alarms/account")
def account_info():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id": session['user_id']
    }
    return render_template("account_info.html", user = User.get_one(data))

@app.route("/alarms/contact")
def contact():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id": session['user_id']
    }
    return render_template("contact.html", user = User.get_one(data))

@app.route("/alarms/take_breaks")
def taking_breaks():
    if 'user_id' not in session:
        return render_template("taking_breaks.html")
    data = {
        "id": session['user_id']
    }
    return render_template("taking_breaks.html", user = User.get_one(data))




@app.route('/register', methods=['POST'])
def register():
    if not User.register_valid(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password" : pw_hash
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    return redirect('/alarms')


@app.route('/login', methods=['POST'])
def login():
    data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email/password", "login")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/password", "login")
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect("/alarms")


@app.route('/alarms/account/update', methods=['POST'])
def account_update():
    if not User.account_update_valid(request.form):
        return redirect('/alarms/account')
    data = {
        "id": request.form['id'],
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
    }
    User.update(data)
    return redirect('/alarms')

@app.route('/alarms/account/password', methods=['POST'])
def password_update():
    data = { "id" : request.form["id"] }
    user_in_db = User.get_one(data)
    if not bcrypt.check_password_hash(user_in_db.password, request.form['current_password']):
        flash("Invalid Current Password", "password")
        return redirect('/alarms/account')
    if not User.password_update_valid(request.form):
        return redirect('/alarms/account')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "id": request.form['id'],
        "password" : pw_hash
    }
    User.update_password(data)
    return redirect('/alarms')


@app.route('/alarms/contacted', methods=['POST'])
def alarms_contacted():
    if 'user_id' not in session:
        return redirect('/')
    if not Inquiry.contacted_valid(request.form):
        return redirect("/alarms/contact")
    Inquiry.save(request.form)
    return redirect('/alarms')

@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")
