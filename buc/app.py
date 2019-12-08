from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import SelectField
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os 
from flask import request
import time
  
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////mnt/c/Users/gotom/Desktop/building_user_login_system-master/finish/database.db"
bootstrap = Bootstrap(app)                        

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#資料庫與表單設定-------------------------------------------------------------------------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    winvm=db.Column(db.Integer)
    linvm=db.Column(db.Integer)
    appvm=db.Column(db.Integer)

class vm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vmname=db.Column(db.String)
    service=(db.String)
    disk=(db.String)

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

class vmForm(FlaskForm):
    vmname = StringField('give it a name', validators=[InputRequired(), Length(min=1, max=15)])
    service = SelectField('service', choices=[('win','windows VM'), ('lin','linux VM'),('app','Application')])
    vcpu = SelectField('vcpu', choices=[('1','1'), ('2','2'),('4','4')])
    ram = SelectField('ram', choices=[('1024','1GB'), ('2048','2GB'),('4096','4GB')])
    disk = SelectField('disk', choices=[('30','30G'),('40','40G'),('50','50G'),('60','60G')])


#--主頁/登入/註冊-------------------------------------------------------------------------
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
                print(user.password)
                print(form.password.data)
            
                login_user(user, remember=form.remember.data)
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

#--主控板-------------------------------------------------------------------------------
@app.route('/dashboard',  methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html',Welcome="Welcome,", name=current_user.username, w=str(current_user.winvm), l=str(current_user.linvm), a=str(current_user.appvm))

@app.route('/dashboard/windows',  methods=['GET', 'POST'])
@login_required
def windowsvm_show():
    return render_template('dashboard.html', w=str(current_user.winvm), a='0', l='0')

@app.route('/dashboard/linux',  methods=['GET', 'POST'])
@login_required
def linuxvm_show():
    return render_template('dashboard.html', l=str(current_user.linvm), a='0', w='0')

@app.route('/dashboard/app',  methods=['GET', 'POST'])
@login_required
def appvm_show():
    return render_template('dashboard.html',a=str(current_user.appvm), w='0', l='0')

  
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

#--啟動vm--------------------------------------------------------------------------------
@app.route('/launch',  methods=['GET', 'POST'])
# @login_required
def launch():
    return render_template('vmshow.html', vmurl="http://192.168.69.112:8080/guacamole-0.9.14/#/client/a2FpX3dpbjEwAGMAbm9hdXRo")

    
#--vm渲染--------------------------------------------------------------------------------
@app.route('/winvm', methods=['GET', 'POST'])
def win_data():
    return render_template('winVM.html',name="win10")
    # time.sleep(1)
    
@app.route('/linvm', methods=['GET', 'POST'])
def lin_data():
    return render_template('linVM.html',name="linux")
    # time.sleep(3)

@app.route('/appvm', methods=['GET', 'POST'])
def app_data():
    return render_template('appVM.html',name="app")
    # time.sleep(3)

#--新增vm-------------------------------------------------------------------------------
@app.route('/new', methods=['GET', 'POST'])
def new():
    form=vmForm()
    if form.validate_on_submit():
        new_vm = vm(vmname=form.vmname.data, service=form.service.data, disk=form.disk.data)
        db.session.add(new_vm)
        db.session.commit()

        return '<h1>New VM has been created!</h1>'
    return render_template('new.html', name="Creat a new serivce!", form=form)
    # time.sleep(3)



if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0')