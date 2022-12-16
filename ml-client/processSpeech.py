import soundfile as sf
import torch
from datasets import load_dataset
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')
API_URL = "https://api-inference.huggingface.co/models/facebook/wav2vec2-large-960h-lv60-self"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.request("POST", API_URL, headers=headers, data=data)
    return json.loads(response.content.decode("utf-8"))

def transcribe():
    print(query("testsample.m4a"))

transcribe()