from converOpenAI import openAI
from processSpeech import transcribe
from flask import Flask
import requests

app = Flask(__name__)

@app.route('/')
def containerSetUp():
    return 'Contianer is set up!'

@app.route('/transcribe/<filename>')
def transcriber(filename):
    return transcribe(str(filename))

@app.route('/openAI/<prompt>')
def openAIResponse(prompt):
    return openAI(str(prompt))

## app.run(host=HOSTNAME, port=PORT, debug=True)
if __name__ == "__main__":
    app.run(debug=True)