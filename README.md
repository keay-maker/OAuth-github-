see APP!  https://keayoauthh-873cf3b46690.herokuapp.com/


This Flask application is designed to handle user authentication and integrate GitHub OAuth for login. Here's a detailed summary of how it works:

Imports:

The application imports necessary libraries including Flask for web framework, SQLAlchemy for ORM, Flask-Login for session management, and Authlib for OAuth integration.
It also imports os to access environment variables.
Flask App Initialization:

app = Flask(__name__): Creates an instance of the Flask application.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.db': Configures the application to use an SQLite database named login.db.
app.secret_key = os.getenv('APP_SECRET_KEY', 'default_fallback_secret_key'): Sets the secret key for session management, using an environment variable if available, otherwise a default value.
SQLAlchemy Initialization:

db = SQLAlchemy(app): Initializes SQLAlchemy with the Flask app, enabling ORM capabilities.
LoginManager Initialization:

login_manager = LoginManager(app): Initializes the LoginManager with the Flask app to handle user sessions.
login_manager.login_view = 'login': Sets the login view route, which is the endpoint users will be redirected to if they need to log in.

User Model Definition:

class User(db.Model, UserMixin): Defines a User model that inherits from SQLAlchemy's db.Model and Flask-Login's UserMixin.
id = db.Column(db.Integer, primary_key=True): Defines the primary key for the User model.
email = db.Column(db.String(256), unique=True): Defines a unique email field for the User model.
username = db.Column(db.String(256), unique=True): Defines a unique username field for the User model.
User Loader Function:

@login_manager.user_loader: Decorator to define the user loader function.
def load_user(user_id): Function to load a user by their ID.
return User.query.get(int(user_id)): Queries the User model by ID and returns the user instance.
OAuth Initialization:

oauth = OAuth(app): Initializes OAuth with the Flask app.
github = oauth.register(...): Registers the GitHub OAuth client using environment variables for the client ID and other necessary configurations.
