from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
import json
from dotenv import load_dotenv
from flask_mail import Mail
import os
from werkzeug.utils import secure_filename

# Loading env variables
load_dotenv()

GMAIL_USERNAME = os.getenv("GMAIL_USERNAME")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
SECRET_KEY = os.getenv("SECRET_KEY")

with open("config.json", "r") as c:
    params = json.load(c)["params"]

local_server = params["local_server"]

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")
app.config['UPLOAD_FOLDER'] = params["upload_location"]

# Connecting with smtp server
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 465,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = GMAIL_USERNAME,
    MAIL_PASSWORD = GMAIL_PASSWORD
)
mail = Mail(app)

if(local_server):
    app.config["SQLALCHEMY_DATABASE_URI"] = params["local_uri"]
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = params["prod_uri"]

db = SQLAlchemy(app)

class Contacts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=True, default=lambda: datetime.now(timezone.utc))

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    sub_title = db.Column(db.String(255), nullable=True)
    slug = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    excerpt = db.Column(db.String(500), nullable=True)
    content = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, nullable=True, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=True, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

@app.route("/")
def home_default():
    posts= Posts.query.filter_by().all()

    return render_template('index.html', params=params, posts=posts)

@app.route("/index.html")
def home_nav():
    posts= Posts.query.filter_by().all()

    return render_template('index.html', params=params, posts=posts)

@app.route("/about.html")
def about():
    return render_template('about.html', params=params)

@app.route("/contact.html", methods= ['GET', 'POST'])
def contact():
    if(request.method == 'POST'):
        '''Add entry to the database'''
        name= request.form.get('name')
        email= request.form.get('email')
        phone= request.form.get('phone')
        message= request.form.get('message')

        entry= Contacts(name=name, phone=phone, email=email, message=message)
        db.session.add(entry)
        db.session.commit()

        # Sending mail
        mail.send_message('New message from Blog',
                          sender=email,
                          recipients=[GMAIL_USERNAME],
                          body = message + '\n' + name + '\n' + phone
                          )

        # Render the template directly to pass the success variable
        return render_template('contact.html', success=True, params=params)

    return render_template('contact.html', params=params)

# Routing Posts
@app.route("/post/<string:post_slug>", methods=['GET'])
def post(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first_or_404()

    return render_template('post.html', params=params, post=post)

# Dashboard
@app.route("/dashboard", methods= ['GET', 'POST'])
def dashboard():
    # 1. Check if the user is ALREADY logged in
    if 'user' in session and session['user'] == ADMIN_EMAIL:
        posts = Posts.query.all()
        # Render the new admin dashboard template!
        return render_template('admin.html', params=params, posts=posts)
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if(email == ADMIN_EMAIL and password == ADMIN_PASSWORD):
            # 2. Set the session variable
            session['user'] = email
            # Redirect back to the dashboard via a fresh GET request
            return redirect('/dashboard')
        else:
            # Pass an error message to the template!
            return render_template('login.html', params=params, error="Invalid email or password. Please try again.")

    # 3. If it's a GET request and they aren't logged in, show the login page
    return render_template('login.html', params=params)

# Edit Post
@app.route("/edit/<string:id>", methods= ['GET', 'POST'])
def post_edit(id):

    # Check if the user is ALREADY logged in
    if 'user' in session and session['user'] == ADMIN_EMAIL:

        # 2. Fetch the existing post if we are editing (not creating new)
        if id != '0':
            post = Posts.query.filter_by(id=id).first()
        else:
            post = None

        if(request.method == 'POST'):
            title= request.form.get('title')
            sub_title= request.form.get('sub_title')
            slug= request.form.get('slug')
            author= request.form.get('author')
            content= request.form.get('content')

            # Catch the uploaded Header Image
            image_file = request.files.get('image')
            image_name = None

            # If the user actually selected a new file to upload
            if image_file and image_file.filename != '':
                image_name = secure_filename(image_file.filename)
                # Save it
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], image_name)
                image_file.save(filepath)

            # If we are editing an existing post and DID NOT upload a new image, keep the old one!
            if id != '0' and not image_name:
                image_name = post.image

            # Create a NEW post
            if id=='0':
                entry= Posts(title=title, sub_title=sub_title, slug=slug, content=content, author=author, image=image_name)
                db.session.add(entry)
                db.session.commit()
            else:
                # UPDATE an existing post
                post.title = title
                post.sub_title = sub_title
                post.slug = slug
                post.author = author
                post.content = content
                post.image = image_name
                db.session.commit()

            # Redirect back to the dashboard after saving!
            return redirect('/dashboard')
        
        # 3. Render the template securely inside the authentication block
        return render_template('edit.html', params=params, post=post, id=id)
    
    # 4. If they aren't logged in, redirect them away
    return redirect('/dashboard')

# Logout
@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect('/dashboard')

if __name__ == '__main__':
    app.run(debug=True)