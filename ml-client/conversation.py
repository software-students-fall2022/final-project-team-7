import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')

API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

def chat():
    while True:
        text = input(">>> ")
        if text == "stop":
            break
        payload = {"inputs": text}
        response = query(payload)
        print(response["generated_text"])

chat()