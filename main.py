from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3adfB'

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.String(5000))

    def __init__(self, title, body):
        self.title = title
        self.body = body
        
class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    tasks = db.relationship('Task', backref='owner')

    def __init__(self, email, password):
        self.email = email
        self.password = password



@app.route('/blog', methods=['GET','POST'])
def index():
    blog_query = Blog.query.all()

    if request.args:
        id = request.args.get('id')
        blog = Blog.query.get(id)
        return render_template('blog.html',blog=blog)
    
    
    return render_template('blog.html',blog_query=blog_query)
    



@app.route('/newpost', methods=['POST', 'GET'])
def post():


    title = ''
    body = ''
    error = ''


    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']


        
        if len(title) == 0 or len(body) == 0:
            error = "Both fields must me filled out"
            return render_template('newpost.html',title=title,body=body,error=error)

    


        new_title = Blog(title, body)
        db.session.add(new_title)
        db.session.commit()

        id = new_title.id
        return redirect('/blog?id=' + str(id))


    return render_template('newpost.html', title=title, body=body)




if __name__ == '__main__':
    app.run()