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
from editXML import modXML

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

class vm(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vmname=db.Column(db.String)
    service=db.Column(db.String(15))
    disk=db.Column(db.String(5))
    address=db.Column(db.String)

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

class urlForm(FlaskForm):
    url_name=StringField

#--主頁/登入/註冊-------------------------------------------------------------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))

        return '<h1>Invalid username or password</h1>'

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

    return render_template('signup.html', form=form)

#--主控板選項-------------------------------------------------------------------------------
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
url='/'
@app.route('/launch',  methods=['GET', 'POST'])
# @login_required
def launch():
    global url
    guaca_url="http://guacamole/"
    if request.method == 'POST':
        url=request.form['name']
        print(url)
        return redirect(url_for('dashboard'))
        
    if request.method == 'GET':    
        return render_template('vmshow.html', vmurl=guaca_url+url)
   
#--vm渲染--------------------------------------------------------------------------------
@app.route('/winvm', methods=['GET', 'POST'])
def win_data():
    total = current_user.winvm
    win_data.cnt += 1

    query = vm.query.filter_by(id=win_data.cnt).first()
    while(query.service!='win'):
        win_data.cnt +=1
        query = vm.query.filter_by(id=win_data.cnt).first()

    win_data.cnt2+=1
    if(win_data.cnt2==total):
        win_data.cnt2=0
        win_data.cnt=0

    return render_template('winVM.html',name=query.vmname) 
win_data.cnt = 0
win_data.cnt2 = 0
    
@app.route('/linvm', methods=['GET', 'POST'])   
def lin_data():
    total = current_user.linvm
    lin_data.cnt += 1

    query = vm.query.filter_by(id=lin_data.cnt).first()
    while(query.service!='lin'):
        lin_data.cnt +=1
        query = vm.query.filter_by(id=lin_data.cnt).first()
    
    lin_data.cnt2+=1
    if(lin_data.cnt2==total):
        lin_data.cnt2=0
        lin_data.cnt=0

    return render_template('linVM.html',name=query.vmname)
lin_data.cnt = 0
lin_data.cnt2 = 0

@app.route('/appvm', methods=['GET', 'POST'])
def app_data():
    total = current_user.appvm
    app_data.cnt += 1

    query = vm.query.filter_by(id=app_data.cnt).first()
    while(query.service!='app'):
        app_data.cnt +=1
        query = vm.query.filter_by(id=app_data.cnt).first()
    
    app_data.cnt2+=1
    if(app_data.cnt2==total):
        app_data.cnt2=0
        app_data.cnt=0

    return render_template('appVM.html',name=query.vmname)
app_data.cnt = 0
app_data.cnt2 = 0


#--新增vm-------------------------------------------------------------------------------
@app.route('/new', methods=['GET', 'POST'])
def new():
    form=vmForm()
    if form.validate_on_submit():
        new_vm = vm(vmname=form.vmname.data, service=form.service.data, disk=form.disk.data, address="http://192.168.69.112:8080/guacamole-0.9.14/#/client/"+form.vmname.data)
        db.session.add(new_vm)
        db.session.commit()
        
        if(form.service.data=='win'):
            query = User.query.filter_by(username=current_user.username).first()
            query.winvm = current_user.winvm+1
            db.session.commit()
        if(form.service.data =='lin'):    
            query = User.query.filter_by(username=current_user.username).first()
            query.linvm = current_user.linvm+1
            db.session.commit()
        if(form.service.data =='app'):    
            query = User.query.filter_by(username=current_user.username).first()
            query.appvm = current_user.appvm+1
            db.session.commit()

        #執行.sh新增openstack vm 並且抓取vm ip
        output = os.popen('./ip.sh')
        # print(output.read())
        #拿vmip去更新xml檔案
        path='/mnt/c/Users/gotom/Desktop/desk.xml'
        ip=output.read()
        modXML(path,form.vmname.data,ip,form.service.data)

        # return '<h1>New VM has been created!</h1>'
        time.sleep(2)
        return redirect(url_for('dashboard'))

        
    return render_template('new.html', name="Creat a new serivce!", form=form)
    # time.sleep(3)



if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0')