
# Setup:

install all required dependacies

```bash
pip install -r requirements.txt
```

Create a OpenAi account
get an API key
 
**Create a `.env` file:** In your project directory, create a file named `.env` if it doesn't already exist.

**Add your OpenAI API key to the `.env` file:** Open the `.env` file with a text editor, and add the following line:
`OPENAI_API_KEY=your_openai_api_key_here`
    Replace `your_openai_api_key_here` with your actual OpenAI API key.
same for pinecone
`PINECONE_API_KEY=yourapi_key_here`

in Pinecone site create a new index
name it `lawyer`
set dimensions to 384

open processing.ipynb and run all

run app.py

if you don't want to pay for Open Ai api or set up anything before this run app.py

log in using 
username : `DEMO`
password : `DEMO`

these chats were real and saved