from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
import json

with open("config.json", "r") as c:
    params = json.load(c)["params"]

local_server = params["local_server"]

app = Flask(__name__)

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

@app.route("/")
def home_default():
    return render_template('index.html', params=params)

@app.route("/index.html")
def home_nav():
    return render_template('index.html', params=params)

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

        # Render the template directly to pass the success variable
        return render_template('contact.html', success=True, params=params)

    return render_template('contact.html', params=params)

@app.route("/post.html")
def post():
    return render_template('post.html', params=params)

if __name__ == '__main__':
    app.run(debug=True)