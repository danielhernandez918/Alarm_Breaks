from flask_app import app
from flask import render_template, request, redirect, session
from flask import flash
from flask_app.models.user import User
from flask_app.models.alarm import Alarm


@app.route('/alarms/new')
def alarms_new():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id": session['user_id']
    }
    return render_template("new_alarm.html", user=User.get_one(data)) 

@app.route('/alarms/edit/<int:id>')
def alarms_edit(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id": id
    }
    return render_template("edit_alarm.html", alarm=Alarm.get_one(data)) 

@app.route('/alarms/view_alarm/<int:id>')
def alarms_view(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id": id
    }
    return render_template("alarm_view.html", alarm=Alarm.get_one(data)) 




@app.route('/alarms/create', methods=['POST'])
def alarms_create():
    if 'user_id' not in session:
        return redirect('/')
    if not Alarm.alarm_valid(request.form):
        return redirect("/alarms/new")
    Alarm.save(request.form)
    return redirect('/alarms')

@app.route('/alarms/update', methods=['POST'])
def alarms_update():
    if 'user_id' not in session:
        return redirect('/')
    if not Alarm.alarm_valid(request.form):
        return redirect(f"/alarms/edit/{request.form['id']}")
    Alarm.update(request.form)
    return redirect('/alarms')

@app.route("/alarms/delete/<int:id>")
def alarms_delete(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id" : id
    }
    Alarm.delete(data)
    return redirect('/alarms')

@app.route('/alarms/activate', methods=['POST'])
def alarms_activate():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "hour": request.form['hour'],
        "minute": request.form['minute'],
        "ampm": request.form['ampm']
    }
    Alarm.alarm(data)
    return redirect('/alarms')
