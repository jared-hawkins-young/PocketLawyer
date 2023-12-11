from flask import Flask, render_template, request, session, redirect, url_for,jsonify
import utils
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()
app = Flask(__name__, static_url_path='', static_folder='templates')

app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    chats = db.relationship('Chat', backref='user')

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timeid = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(80))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    messages = db.relationship('Message', backref='chat')

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'))
    content = db.Column(db.String(100000), nullable=False)




@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    # Get the entered username and password from the form
    entered_username = request.form['username']
    entered_password = request.form['password']

    # Check if the username and password are correct
    user = User.query.filter_by(username=entered_username, password=entered_password).first()
    print(user)

    if user:
        # Set the session variable to indicate a successful login
        session['logged_in'] = True
        session['username'] = entered_username
        return redirect(url_for('chatbot'))
    else:
        # Redirect back to the login page if the credentials are incorrect
        return redirect(url_for('home'))


@app.route('/chatbot')
def chatbot():
    # Check if the user is logged in before rendering the chatbot page
    try:
        if session['logged_in']:
            return render_template('chatbot.html')
        else:
            return redirect(url_for('home'))
    except KeyError:
        return redirect(url_for('home'))
    
@app.route('/logout')
def logout():
    
    
    
    
    # Clear the session variable to indicate a logout
    
    
    session['logged_in']=False
    return redirect(url_for('home'))
 

@app.route('/get_response', methods=['POST'])
def get_response():
    history_string = request.form['history']
    
    # Split the history string into individual entries
    entries = history_string.split('\n')
    
    # Extract the message (last entry) and the remaining history
    if entries:
        message = entries.pop().split(': ')[1] if entries[-1].startswith('user:') else ''
    
    # Reconstruct the updated history string
    updated_history = '\n'.join(entries)
    
    # Generate a response to the user message
    history = {}
    response = utils.chatbot_response(message, history,updated_history)
    
    return jsonify({'bot_response': response})

@app.route('/create_user', methods=['POST','GET'])
def create_user():
    # Connect to the database
    if request.method == 'POST':
        
        username = request.form['username']
        password = request.form['password']
    
        # Create a new user object
        new_user = User(username=username, password=password)
    
        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()
    
        return redirect(url_for('home'))
    else:
        return render_template('create_user.html')
    

    
@app.route('/load_chat', methods=['GET'])
def load_chat():
    # Get the username from the session
    username = session['username']
    
    # Get the user object from the database
    user = User.query.filter_by(username=username).first()
    
    # Get the chat history for the user
    chats = Chat.query.filter_by(user_id=user.id).all()
    
    # Create a list of chat names and ids
    chat_list = []
    for chat in chats:
        message = Message.query.filter_by(chat_id=chat.id).first()
        chat_list.append({'name': chat.name, 'id': chat.timeid , 'messages': message.content})
    
    
    return jsonify({'chats': chat_list})

@app.route('/remove_chat', methods=['POST'])
def remove_chat():
    # Get the username from the session
    username = session['username']
    
    # Get the user object from the database
    user = User.query.filter_by(username=username).first()
    
    # Get the chat id from the request
    timeid = request.form['id']
    
    # Get the chat from the database
    chat = Chat.query.filter_by(timeid=timeid, user_id=user.id).first()
    
    # Delete the chat from the database
    db.session.delete(chat)
    db.session.commit()
    
    return jsonify({'response': 'ok'})
        



@app.route('/save_chat', methods=['POST'])
def save_chat():
    # Get the username from the session
    username = session['username']
    
    # Get the user object from the database
    user = User.query.filter_by(username=username).first()
    
    # Get the chat history from the request
    chat_history = request.form['history']
    
    # Get the timeid from the request
    timeid = request.form['id']
    
    # Check if a chat with the same timeid already exists
    existing_chat = Chat.query.filter_by(timeid=timeid, user_id=user.id).first()

    if existing_chat:
        # Update the existing chat
        existing_chat.name = request.form['name']
        existing_chat.timeid = timeid
        db.session.commit()
        # Update the associated message
        existing_message = Message.query.filter_by(chat_id=existing_chat.id).first()
        if existing_message:
            existing_message.content = chat_history
            db.session.commit()
    else:
        # Create a new chat
        new_chat = Chat(name=request.form['name'], timeid=timeid, user_id=user.id)
        db.session.add(new_chat)
        db.session.commit()
        # Create a new message associated with the new chat
        new_message = Message(content=chat_history, chat_id=new_chat.id)
        db.session.add(new_message)
        db.session.commit()

    return jsonify({'response': 'ok'})


if __name__ == '__main__':
    app.run(debug=True)