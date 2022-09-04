from flask import render_template, redirect, session, request, flash
from flask_bcrypt import Bcrypt
from flask_app import app
from flask_app.models.user import User


BCRYPT = Bcrypt(app)


@app.route('/')
def r_login_and_registration():
    if 'user_id' in session:
        return redirect('/recipes')
    return render_template('login_and_registration.html')


@app.route('/registration', methods=['POST'])
def f_registration():
    if not User.validate_registration(request.form):
        return redirect('/')
    
    registration_data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email_registration'],
        'password': BCRYPT.generate_password_hash(request.form['password_registration'])
    }

    user_id = User.register_user(registration_data)
    session['user_id'] = user_id
    return redirect('/recipes')


@app.route('/login', methods=['POST'])
def f_login():
    if not User.validate_login(request.form):
        return redirect('/')
    
    login_data = {
        'email': request.form.get('email_login'),
        'password': request.form.get('password_login') 
    }

    user = User.get_by_email(login_data)
    pw_check = BCRYPT.check_password_hash(user.password, login_data['password'])
    if not pw_check:
        flash('* Invalid password.', 'login')
        return redirect('/')

    session['user_id'] = user.id
    return redirect('/recipes')


@app.route('/logout')
def f_logout():
    session.clear()
    return redirect('/')