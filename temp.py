from flask import Flask, render_template, request

app = Flask(__name__, static_url_path='', static_folder='templates')

@app.route('/')
def home():
    return render_template('chatbot.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.form['user_message']
    bot_response = f"You said: {user_message}"
    chat_history = [{'type': 'user', 'message': user_message}, {'type': 'bot', 'message': bot_response}]
    return {'bot_response': bot_response, 'chat_history': chat_history}

if __name__ == '__main__':
    app.run(debug=True)