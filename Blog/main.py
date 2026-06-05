from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home_default():
    return render_template('index.html')

@app.route("/index.html")
def home_nav():
    return render_template('index.html')



@app.route("/about.html")
def about():
    return render_template('about.html')


@app.route("/contact.html")
def contact():
    return render_template('contact.html')


@app.route("/post.html")
def post():
    return render_template('post.html')

if __name__ == '__main__':
    app.run(debug=True)