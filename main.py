from flask import  request
import datetime  , json
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
# from flask_mysqldb import MySQL
# using flaskmail to send email to our email id as well

app=Flask(__name__)

with open("config.json" ,'r') as c :

    params =json.load(c)['params']

app.config.update(
        MAIL_SERVER='smtp.gmail.com',
        MAIL_PORT='465',
        MAIL_USE_SSL=True,
        MAIL_USERNAME=params['gmail-user'],
        MAIL_PASSWORD=params['gmail-password']
    )
mail=Mail(app)      
local_server = True
if (local_server) :
     app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
     print(params['local_uri'])
else:
       app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']
# //pip install mysql-connector-python// download abinary wheeel file to run the sql
# to connect ith prod using idgitial ocean s
db = SQLAlchemy(app)

class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),  nullable=False)
    phone_num = db.Column(db.String(12), unique=True, nullable=True)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120),  nullable=False)

class Posts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80),  nullable=False)
    slug = db.Column(db.String(12), nullable=False)
    content = db.Column(db.String(250), nullable=False)
    tagline = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(14), nullable=True )
    img_file = db.Column(db.String(14), nullable=True )

@app.route("/")
def home():
    posts = Posts.query.filter_by().all()[0:params['no_of_posts']]
    # posts will fetch value from db
    return render_template('index.html',params=params,posts=posts)


@app.route("/about")
def about():
    return render_template('about.html',params=params)

@app.route("/dashboard")
def about():
    return render_template('login.html',params=params)


@app.route("/post/<string:post_slug>",methods=['GET'])
def  post_route(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()
    return render_template('post.html', params=params ,post=post)
## post = post it mean it can travel to html page and from ther we can access multiple attributes using db

@app.route("/contact" ,methods =['GET','POST'])
def contact():
    if (request.method =="POST"):
        ''' Add entry to the database'''
        name=request.form.get('name')
        phone=request.form.get('phone')
        message=request.form.get('message')
        date=request.form.get('date')
        email= request.form.get('email')

        entry=Contacts(name=name,phone_num=phone,msg=message, date=datetime.datetime.now(),email=email)
        db.session.add(entry)
        db.session.commit()
        mail.send_message("New Message from " + name ,
                          sender=email,
                          recipients=[params['gmail-user']],
                          body = message + "\n" + phone )

    return render_template('contact.html' , params=params)



app.run(debug=True)


## post request syntax in flask   online
