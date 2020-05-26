"""
------------------------------------------ Imports ------------------------------------------
"""
from flask import render_template, Blueprint, request, redirect, url_for, flash
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash

from radzblog import db
from radzblog.models import User
from radzblog.users.forms import RegisterForm, LoginForm, UpdateForm
from radzblog.users.pic_handler import add_profile_pic


"""
----------------------------------------- Blueprint -----------------------------------------
"""
users = Blueprint('users', __name__)


"""
------------------------------------------- Views -------------------------------------------
"""
@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password = form.password.data

        if User.query.filter_by(email=email).first():
            flash(u"Email ID is already registered with us!", "danger")
            return render_template('register.html', form=form)

        elif User.query.filter_by(username=username).first():
            flash(u"Username not available! Please select different username.", "danger")
            return render_template('register.html', form=form)

        else:
            user = User(email=email, username=username, password=password)
            db.session.add(user)
            db.session.commit()
            flash(u"Registered successfully! Please login to your account.", "success")

        return redirect(url_for('users.login'))

    else:
        for field in form.errors:
            if field != "csrf_token":
                for error in form.errors[field]:
                    flash(error, "danger")

        return render_template('register.html', form=form)

    return render_template('register.html', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user.check_password(form.password.data):
            flash(u"Incorrect password entered! Please enter correct password.", "danger")
            return render_template('login.html', form=form)

        if user is not None:
            login_user(user)
            flash(u"Logged in successfully!", "success")

            next = request.args.get('next')
            if next == None or not next[0]=='/':
                next = url_for('core.home')

            return redirect(next)

    else:
        for field in form.errors:
            if field != "csrf_token":
                for error in form.errors[field]:
                    flash(error, "danger")

    return render_template('login.html', form=form)


@users.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u"Logged out successfully!", "success")
    return redirect(url_for('core.home'))


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateForm()

    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password = form.password.data
        picture = form.picture.data

        if User.query.filter_by(email=email).first():
            flash(u"Email ID is already registered! Cannot update your email.", "danger")
            return render_template('account.html', form=form)

        elif User.query.filter_by(username=username).first():
            flash(u"Username not available! Please provide different username.", "danger")
            return render_template('acount.html', form=form)

        elif email or username or password or picture:
            current_user.email = email or current_user.email
            current_user.username = username or current_user.username

            if password:
                current_user.password_hash = generate_password_hash(password)
            
            if picture:
                pic = add_profile_pic(current_user.username, picture)
                current_user.profile_img = pic

            db.session.commit()
            flash(u"Account details updated successfully!", "success")

        return redirect(url_for('users.account'))
    
    else:
        for field in form.errors:
            if field != "csrf_token":
                for error in form.errors[field]:
                    flash(error, "danger")

    return render_template('account.html', form=form)


@users.route('/userblogs/<int:id>')
def userblogs(id):
    user = User.query.get(id)
    return render_template('userblogs.html', user=user)