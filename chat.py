import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_sqlalchemy import SQLAlchemy
from flask import Flask,render_template, redirect, url_for,flash
from passlib.hash import pbkdf2_sha256
from wtform_fields import *
from models import *
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_socketio import SocketIO,send,emit, join_room, leave_room

# Import the class `Flask` from the `flask` module, written by someone else.
app = Flask(__name__)

# Check for environment variable


app.secret_key = os.environ.get('SECRET')
app.config['WTF_CSRF_SECRET_KEY'] = b'_5#y2L"F4Q8z\n\xec]/'
 # Instantiate a new web application called `app`, with `__name__` representing the current file
#Configure database

app.config['SQLALCHEMY_DATABASE_URI']=os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configure session to use filesystem




# Set up database
engine = create_engine('postgresql://me@localhost/mydb',pool_size=30, max_overflow=-1)
db = scoped_session(sessionmaker(bind=engine))
# Set up database
db = SQLAlchemy(app)
# database engine object from SQLAlchemy that manages connections to the database
#Instantiate flask sockerio
socketio = SocketIO(app)
ROOMS = ["Bollywood", "news", "games", "coding"]
# create a 'scoped session' that ensures different users' interactions with the
# database are kept separate

# A decorator; when the user goes to the route `/`, exceute the function immediately below
#Now to connect to the database
#Configure flask login
login = LoginManager(app)
login.init_app(app)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route("/",methods=["GET","POST"])
def index():

    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data
        # Hashing the password that we got from user for security purposes.
        # Hashed password
        hashed_pswd = pbkdf2_sha256.hash(password)
        #Checking if the user exists
        #user_object = User.query.filter_by(username=username).first()
        #if user_object:
            #return "Username alerady taken!"
        user = User(username=username, password=hashed_pswd)
        db.session.add(user)
        db.session.commit()
        flash('Registered successfully. Please login.', 'success')
        return redirect(url_for('login'))


    return render_template("index.html", form=reg_form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    #Allow login if validate_on_submit
    if login_form.validate_on_submit():
        user_object = User.query.filter_by(username=login_form.username.data).first()
        login_user(user_object)
        return redirect(url_for('chat'))



    return render_template("login.html", form=login_form)

@app.route("/chat", methods=['GET','POST'])
@login_required
def chat():
    #if not current_user.is_authenticated:
        #return redirect(url_for('login'))

    return render_template('chat.html',username=current_user.username, rooms=ROOMS)

@app.route("/logout", methods=['GET'])
def logout():
    logout_user()
    flash('You have logged out successfully', 'success')
    return redirect(url_for('login'))
#adding events
@socketio.on('message')
# recieving message in the form of data
def message(data):
    print(f"\n\n{data}\n\n")
    #To broacast this message to frnds or other users!
    send({'msg': data['msg'] , 'username': data['username'] },room=data['room'] )
    #To specify which event bucket we want to send data , we use emit
    #emit('event', "This is a custom event message")

@socketio.on('join')
def join(data):
    join_room(data['room'])
    send({'msg': data['username'] + " has joined the " + data['room'] + " room."}, room=data['room'])

@socketio.on('leave')
def leave(data):
    leave_room(data['room'])
    send({'msg': data['username'] + "has left the " + data['room'] + "room"}, room=data['room'])
if __name__ == "__main__":
    #socketio.run(app, debug=True)
    app.run()
#debug = True will restart the server everytime we make changes
