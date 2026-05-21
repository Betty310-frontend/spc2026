from flask import Flask, render_template, request

import openai

from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')
openai_model = os.getenv('OPENAI_MODEL')

client = openai.OpenAI(api_key=openai_api_key)

def ask_chatbot(user_input):
    response = client.responses.create(
        model=openai_model,
        instructions="You are a helpful assistant. Please provide advice based on the user's input.",
        input=user_input,
    )
    return response.output_text

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')