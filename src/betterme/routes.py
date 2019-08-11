import os
from flask import render_template, url_for, flash, redirect, request
from betterme.models import User,Survey
from betterme.forms import RegistrationForm, LoginForm, UpdateAccountForm
from betterme import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required

surveys = [
    {
        'author': 'John Kim',
        'questionText' : 'What is my weakness?',
        'answerText' : 'Faithfulness',
        'dateCompleted':'June 3rd, 2019'
    },
    {
        'author': 'Lisa Flechon',
        'questionText' : 'What is my strength?',
        'answerText' : 'I think you are very g',
        'dateCompleted':'June 3rd, 2019'
    }
]

# @app.route("/")
@app.route('/')
def home():
    return render_template('home.html', surveys = surveys)

@app.route('/about')
def about():
    return render_template('about.html',title = 'About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/account", methods = ['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        # current_user.username = form.username.data
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        db.session.commit()
        flash('Your account has been updated!','success')
        return redirect(url_for('account'))
    image_file = url_for('static',filename = 'profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file= image_file, form = form)