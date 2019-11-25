from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os 
from flask import request
  
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////mnt/c/Users/gotom/Desktop/building_user_login_system-master/finish/database.db"
bootstrap = Bootstrap(app)                        
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        # os.system('"/mnt/c/Program Files (x86)/google/Chrome/Application/chrome.exe" http://192.168.69.112:8080/guacamole/#/client/a2FpX3dpbjEwAGMAZGVmYXVsdA==')
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                # os.system('"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" http://192.168.69.112:8080/guacamole/#/client/a2FpX3dpbjEwAGMAZGVmYXVsdA==') 
                return redirect(url_for('dashboard'))

        return '<h1>Invalid username or password</h1>'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return '<h1>New user has been created!</h1>'
        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('signup.html', form=form)

@app.route('/dashboard',  methods=['GET', 'POST'])
@login_required
def dashboard():
    # if request.method=='POST':
    #     os.system('"/mnt/c/Program Files (x86)/google/Chrome/Application/chrome.exe" http://192.168.69.112:8080/guacamole/#/client/a2FpX3dpbjEwAGMAZGVmYXVsdA==')
    return render_template('dashboard.html', name=current_user.username)
    # return render_template('winVM.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/launch',  methods=['GET', 'POST'])
# @login_required
def launch():
    # if request.method=='POST':
    #     print("cool")
    os.system('"/mnt/c/Program Files (x86)/google/Chrome/Application/chrome.exe" http://192.168.69.112:8080/guacamole/#/client/a2FpX3dpbjEwAGMAZGVmYXVsdA==')
    # # return render_template('dashboard.html', name=current_user.username)
    # pass
    return redirect(url_for('dashboard'))
    

@app.route('/winvm', methods=['GET', 'POST'])
def win_data():
    return render_template('winVM.html')

@app.route('/linvm', methods=['GET', 'POST'])
def lin_data():
    return render_template('linVM.html')

if __name__ == '__main__':
    app.run(debug=True)
