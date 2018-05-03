"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage.html")

@app.route('/users')
def user_list():
    """Show list of users."""

    users=User.query.all()
    return render_template("user_list.html", users=users)

@app.route('/register')
def register():
    """Register User"""

    return render_template("register_form.html")

@app.route('/registration', methods=['POST'])
def registration():
    """Register user"""

    user_email = request.form['email']
    user_password = request.form['password']

    email_query = User.query.filter_by(email=user_email).all()

    if email_query:
        return redirect("/")
    
    else:
        user = User(email=user_email,
                    password=user_password)

        db.session.add(user)
        db.session.commit()

        # print "this worked"

    return redirect("/")

@app.route('/login-form')
def login_form():
    """Login form"""
    return render_template("login.html")

@app.route('/login', methods=["POST"])
def login_check():
    """Validates user info"""

    user_email = request.form['email']
    user_password = request.form['password']


#try & except or .first and conditional with None
    
    
    email_query = User.query.filter_by(email=user_email).first()
    
    if email_query == None:
        flash('Invalid email or password')
        return redirect('/login-form')

    password_query = User.query.filter_by(password=user_password).all()


    if user_password==email_query.password:

        session['user'] = email_query.user_id
        flash('You were successfully logged in')


        user_id = email_query.user_id
        # doesnt work bc user_id is not define like user_email above with request.form
        # print user_id

        # maybe connect email typed in with user id

        return redirect('/users/%s' % user_id)

    else:
        flash('Invalid')
        return redirect('/login-form')

@app.route('/logout')
def logout():
    session.pop('user')
    flash('You were successfully logged out')

    return redirect('/')

@app.route('/users/<user_id>')
def user_info(user_id):
    """Show user's info"""
    user_id = User.query.filter_by(user_id=user_id).first()

    return render_template("user_info.html", user=user_id)
    # , user= user_id, title=title, rating=rating)

@app.route('/movies')
def display_movies():
    """Show movies"""
    movies = Movie.query.all()
    print movies
    return 'hello'
    # return render_template("list_movies.html", movies=movies)

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
