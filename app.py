from flask import Flask, redirect, url_for, session, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, current_user, login_required, logout_user
from authlib.integrations.flask_client import OAuth
import os

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.db'
app.secret_key = os.getenv('APP_SECRET_KEY', 'default_fallback_secret_key')

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Initialize LoginManager
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Define User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), unique=True)
    username = db.Column(db.String(256), unique=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Initialize OAuth
oauth = OAuth(app)
github = oauth.register(
    name='github',
    client_id=os.getenv('GITHUB_CLIENT_ID'),
    client_secret=os.getenv('GITHUB_CLIENT_SECRET'),
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
    api_base_url='https://api.github.com/',
    userinfo_endpoint='https://api.github.com/user',
    client_kwargs={'scope': 'user:email'},
)

@app.route('/')
@login_required
def index():
    username = dict(session).get('username', None)
    return f'Hello, {username}!'

@app.route('/login')
def login():
    # Dynamically generate the redirect URI
    redirect_uri = url_for('authorize', _external=True)
    return github.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    token = github.authorize_access_token()
    if not token:
        return 'Authorization failed.', 400

    # Fetch user info from GitHub
    resp = github.get('user')
    user_info = resp.json()
    if not user_info:
        return 'Failed to fetch user info.', 400

    # Store user info in the session
    session['email'] = user_info.get('email')
    session['username'] = user_info.get('login')
    session.permanent = True

    # Query or create the user in the database
    email = user_info.get('email')
    username = user_info.get('login')
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(email=email, username=username)
        db.session.add(user)
        db.session.commit()
    login_user(user)

    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    logout_user()
    session.clear()  # Clear all session data
    return redirect('/')

