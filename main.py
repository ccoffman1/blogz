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
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner



class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            return redirect('/newpost')
        else:
            flash('That username and password combination doesn\'t exist.', 'error')

    return render_template('login.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        existing_user = User.query.filter_by(username=username).first()

        # validate user's data
        if (username == "") or (password == "") or (verify == ""):
            flash('All fields must be filled out.')

        elif (len(username) < 3) or (len(password) < 3) or (len(verify) < 3):
            flash('Username and Password must be greater than three characters.')
        
        elif (password != verify):
            flash('Passwords do not match.')
        elif (existing_user):
            flash('That username is already taken.')
        else:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/')


    return render_template('signup.html')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/login')


    
@app.route('/', methods=['POST', 'GET'])
def index():


    owner = User.query.filter_by(username=session['username']).first()
    blog_query = Blog.query.filter_by(owner=owner).all()
    blogs = Blog.query.filter_by(owner=owner).all()

    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']

        new_blog = Blog(blog_title, blog_body, owner)
        db.session.add(new_blog)
        db.session.commit()

    if request.args:
        id = request.args.get('id')
        blog = Blog.query.get(id)
        return render_template('blog.html',blog=blog)

    

    
    return render_template('blog.html',blogs=blogs,blog_query=blog_query)


@app.route('/newpost', methods=['POST', 'GET'])
def post():


    title = ''
    body = ''

    owner = User.query.filter_by(username=session['username']).first()

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
       
        if len(title) == 0 or len(body) == 0:
            flash("Both fields must me filled out",'error')
            return render_template('newpost.html',title=title,body=body)




        new_blog = Blog(title, body, owner)
        db.session.add(new_blog)
        db.session.commit()

        id = new_blog.id
        return redirect('/?id=' + str(id))


    return render_template('newpost.html', title=title, body=body)




if __name__ == '__main__':
    app.run()