from flask import Flask, request, render_template,  jsonify
import openai
import langchain
from pinecone import Index
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Pinecone and OpenAI setup using environment variables
pinecone_api_key = os.getenv('PINECONE_API_KEY')
openai_api_key = os.getenv('OPENAI_API_KEY')
pinecone_index = Index('lawyer')
openai.api_key = openai_api_key
#langchain = langchain()
"""
# Route for the chat interface
@app.route('/')
def chat():
    return render_template('chat.html')

# Route for handling messages
@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.form['message']
    response = generate_response(user_message)
    return response

def generate_response(message):
    try:
        # Assuming you are using GPT-3 models
        response = openai.Completion.create(
            model="text-davinci-003",  # or another appropriate model
            prompt=message,
            max_tokens=50
        )
        return response.choices[0].text
    except Exception as e:
        print(f"Error generating response: {e}")
        return "Sorry, I couldn't process that message."

if __name__ == '__main__':
    app.run(debug=True)"""
    
# Global variable to store conversation history (not ideal for production)
conversation_history = []

@app.route('/')
def chat():
    return render_template('chat.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.form['message']
    conversation_history.append({'role': 'user', 'content': user_message})

    bot_response = generate_response(user_message)
    conversation_history.append({'role': 'bot', 'content': bot_response})

    return jsonify(conversation_history)

def generate_response(message):
    try:
        # Concatenate all messages to form the conversation context
        conversation = "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_history])

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=conversation,
            max_tokens=150,
            stop=None
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error generating response: {e}")
        return "Sorry, I couldn't process that message."

if __name__ == '__main__':
    app.run(debug=True)
