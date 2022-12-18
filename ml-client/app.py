from converOpenAI import openAI
from processSpeech import transcribe
from flask import Flask

app = Flask(__name__)

@app.route('/')
def containerSetUp():
    return 'Contianer is set up!'

@app.route('/transcribe')
def transcribe(fileName):
    return transcribe(fileName)

@app.route('/openAI')
def openAI(conversation):
    return openAI(conversation)

## app.run(host=HOSTNAME, port=PORT, debug=True)
if __name__ == "__main__":
    app.run(debug=True)