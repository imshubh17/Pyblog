from flask import Flask,render_template,request,session,redirect
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime

with open('config.json','r') as c:
    params=json.load(c)["params"]

app = Flask(__name__)
app.secret_key = 'super-key-imshubh-done-mypyblog'

local_server=False
if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['pri_uri']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Post(db.Model):
    __tablename__ ='post'
    sno = db.Column(db.Integer,  primary_key=True, autoincrement=True)
    title = db.Column(db.Text,  nullable=False )
    slug = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.String(50), nullable=True)
    author = db.Column(db.String(20), nullable=True)
    code = db.Column(db.Text, nullable=False)

class Contact(db.Model):
    __tablename__ ='contact'
    id = db.Column(db.Text, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    pn = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    message = db.Column(db.Text, nullable=False)


import math
@app.route("/")
def index():
    posts = Post.query.filter_by().all()
    last=math.ceil(len(posts)/3)
    #[0:params['no_of_posts']]
    #pagination logic
    page = request.args.get('page')
    if not (str(page).isnumeric()):
        page="1"
    page=int(page)
    posts=posts[ (page-1)*3 : (page-1)*3+3]


    if page==1 :
        prev = "#"
        next="/?page="+str(page+1)
    elif page==last:
        prev = "/?page=" + str(page - 1)
        next = "#"
    else:
        prev="/?page=" + str(page - 1)
        next="/?page=" + str(page + 1)

    return render_template('index.html', params=params, posts=posts,nst=next,pre=prev)

@app.route("/about")
def about():
    return render_template('about.html', params=params)


@app.route("/dashboard", methods = ['GET', 'POST'])
def dashboard():

    if ('user' in session and session['user']==params['admin_user']):
        data = Post.query.all()
        return render_template('dashboard.html', params=params,posts=data)
    if request.method=='POST':
        username=request.form.get('uname')
        userpass = request.form.get('pass')
        if (username == params['admin_user'] and userpass == params['admin_password']):
            session['user'] =username
            data = Post.query.all()
            return render_template('dashboard.html', params=params,posts=data)

    return render_template('login.html', params=params)

@app.route("/post/<string:post_slug>", methods=['GET'])
def post_route(post_slug):
    post = Post.query.filter_by(slug=post_slug).first()
    return render_template('post.html', params=params, post=post)

@app.route("/insert", methods = ['GET', 'POST'])
def insert():
    if ('user' in session and session['user']==params['admin_user']):
        if request.method == 'POST':
            box_id=request.form.get('pid')
            box_title =request.form.get('title')
            box_slug =request.form.get('slug')
            box_content =request.form.get('content')
            box_author = request.form.get('author')
            box_code = request.form.get('code')
            date=datetime.now()

            post = Post(title=box_title, slug=box_slug, content=box_content, date=date, author=box_author,code=box_code)
            db.session.add(post)
            db.session.commit()

    return render_template('insert.html', params=params)


@app.route("/edit/<string:sno>", methods=['GET', 'POST'])
def edit(sno):
    if ('user' in session and session['user']==params['admin_user']):
        if request.method == 'POST':
            box_title =request.form.get('title')
            box_slug =request.form.get('slug')
            box_content =request.form.get('content')
            box_author = request.form.get('author')
            box_code = request.form.get('code')
            date=datetime.now()

            post=Post.query.filter_by(sno=sno).first()
            post.title=box_title
            post.slug = box_slug
            post.content = box_content
            post.date = date
            post.author = box_author
            post.code = box_code
            db.session.commit()
            return redirect('/edit/'+sno)

        post = Post.query.filter_by(sno=sno).first()
        return render_template('edit.html', params=params,post=post)


@app.route("/contact",methods=['GET','POST'])
def contact():
    if(request.method=='POST'):
        name=request.form.get('name')
        pn=request.form.get('pn')
        email =request.form.get('email')
        msg =request.form.get('message')
        cid=name[0:2]+pn[0:]+email[0:4]
        entry = Contact(id=cid,name=name, pn=pn, email=email, message=msg)
        db.session.add(entry)
        db.session.commit()
        return redirect('/')
    return render_template('contact.html',params=params)

@app.route("/logout")
def logout():
    session.pop('user')
    return redirect("/dashboard")

@app.route("/delete/<string:sno>", methods=['GET', 'POST'])
def delete(sno):
    if ('user' in session and session['user']==params['admin_user']):
        post = Post.query.filter_by(sno=sno).first()
        db.session.delete(post)
        db.session.commit()

        return redirect("/dashboard")

if __name__ == '__main__':
    app.run(debug=False)