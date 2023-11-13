""" from dotenv import load_dotenv
load_dotenv()  # Load environment variables from a .env file

# app.py

from flask import Flask, request, jsonify, render_template
from document_processing import processing  # Corrected import statement

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('chat.html')

@app.route('/ask', methods=['POST'])
def ask():
    message = request.form['message']
    # Use the run_qa_chain function from processing.py
    response = processing.run_qa_chain(message)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)


    """
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from a .env file

from flask import Flask, request, jsonify, render_template
from document_processing import processing  # Assuming this is your processing module

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('chat.html')

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.json
        message = data['message']
        # Use the run_qa_chain function from processing.py
        response = processing.run_qa_chain(message)
        return jsonify({'message': response})
    except Exception as e:
        print(e)  # For debugging
        return jsonify({'message': 'An error occurred during processing.'})

if __name__ == '__main__':
    app.run(debug=True)
