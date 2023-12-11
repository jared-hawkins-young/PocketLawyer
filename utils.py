from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)
from dotenv import load_dotenv
import os

from sentence_transformers import SentenceTransformer
import pinecone
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
model = SentenceTransformer('all-MiniLM-L6-v2')

pinecone.init(api_key=os.getenv('PINECONE_API_KEY'), environment='gcp-starter')
index = pinecone.Index('lawyer')

def find_match(input):
    input_em = model.encode(input).tolist()
    result = index.query(input_em, top_k=2, includeMetadata=True)
    return result['matches'][0]['metadata']['text']+"\n"+result['matches'][1]['metadata']['text']

def query_refiner(conversation, query):

    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Given the following user query and conversation log, formulate a question that would be the most relevant to provide the user with an answer from a knowledge base.\n\nCONVERSATION LOG: \n{conversation}\n\nQuery: {query}\n\nRefined Query:"},
    ],
    max_tokens=256,
    temperature=0.7,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0)
    return response.choices[0].message.content


def chatbot_response(query, buffer_memory,history):
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=os.getenv('OPENAI_API_KEY'))

    if 'buffer_memory' not in buffer_memory:
        buffer_memory['buffer_memory'] = ConversationBufferWindowMemory(k=3, return_messages=True)

    system_msg_template = SystemMessagePromptTemplate.from_template(template="""Answer the question as truthfully as possible using the provided context, 
    and if the answer is not contained within the text below, say 'I don't know'""")

    human_msg_template = HumanMessagePromptTemplate.from_template(template="{input}")

    prompt_template = ChatPromptTemplate.from_messages([system_msg_template, MessagesPlaceholder(variable_name="history"), human_msg_template])

    conversation = ConversationChain(memory=buffer_memory['buffer_memory'], prompt=prompt_template, llm=llm, verbose=True)

    refined_query = query_refiner(history, query)
    context = find_match(refined_query)
    response = conversation.predict(input=f"Context:\n {context} \n\n Query:\n{query}")

    return response