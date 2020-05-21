from flask import Flask,render_template,request,session,redirect
import json
from datetime import datetime
import pymongo
from bson import ObjectId

with open('config.json','r') as c:
    params=json.load(c)["params"]

app = Flask(__name__)
app.secret_key = 'super-key-imshubh-done-mypyblog'

client = pymongo.MongoClient(params['pri_uri'])
mydb = client["blog"]
mycol = mydb["blog"]
mycont = mydb["contact"]

import math
@app.route("/")
def index():
    x = mycol.find()
    posts = list(x)
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
    x = mycol.find()
    data = list(x)
    if ('user' in session and session['user']==params['admin_user']):
        return render_template('dashboard.html', params=params,posts=data)
    if request.method=='POST':
        username=request.form.get('uname')
        userpass = request.form.get('pass')
        if (username == params['admin_user'] and userpass == params['admin_password']):
            session['user'] =username
            return render_template('dashboard.html', params=params,posts=data)

    return render_template('login.html', params=params)

@app.route("/post/<string:post_slug>", methods=['GET'])
def post_route(post_slug):
    post = mycol.find_one({'slug':post_slug})
    return render_template('post.html', params=params, post=post)

@app.route("/insert", methods = ['GET', 'POST'])
def insert():
    if ('user' in session and session['user']==params['admin_user']):
        if request.method == 'POST':
            box_title =request.form.get('title')
            box_slug =request.form.get('slug')
            box_content =request.form.get('content')
            box_author = request.form.get('author')
            box_code = request.form.get('code')
            date=datetime.now()

            post = {"title":box_title, "slug":box_slug, "content":box_content, "date":date, "author":box_author,"code":box_code}
            mycol.insert_one(post)

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
            udata={"title":box_title,"slug":box_slug,"content":box_content,"code":box_code,"author":box_author,"date":date}
            mycol.update({'_id': ObjectId(sno) }, {'$set':udata})

            return redirect('/edit/'+sno)

        post = list(mycol.find({'_id': ObjectId(sno) }))
        return render_template('edit.html', params=params,post=post)


@app.route("/contact",methods=['GET','POST'])
def contact():
    if(request.method=='POST'):
        name=request.form.get('name')
        pn=request.form.get('pn')
        email =request.form.get('email')
        msg =request.form.get('message')
        data = {"name": name, "phoneNo": pn, "email": email, "message": msg}
        mycont.insert_one(data)
        return redirect('/')
    return render_template('contact.html',params=params)

@app.route("/logout")
def logout():
    session.pop('user')
    return redirect("/dashboard")

@app.route("/delete/<string:sno>", methods=['GET', 'POST'])
def delete(sno):
    if ('user' in session and session['user']==params['admin_user']):
        mycol.delete_one({'_id': ObjectId(sno)})
        return redirect("/dashboard")

if __name__ == '__main__':
    app.run(debug=False)