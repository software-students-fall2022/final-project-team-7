import os
from converOpenAI import openAI
from processSpeech import transcribe
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/')
def containerSetUp():
    return 'Contianer is set up!'


@app.route('/transcribe', methods=['POST'])
def transcriber():
    data = request.json
    file_name = data["file_name"]

    file_abs_path = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), "../web-client/audios", file_name)

    if os.path.isfile(file_abs_path):
        transcript = transcribe(file_abs_path)

        if "error" in transcript:
            return jsonify({
                "success": 0,
                "message": transcript["error"]
            })
        else:
            return jsonify({
                "success": 1,
                "transcript": transcript
            })
    else:
        return jsonify({
            "success": 0,
            "message": "File not found"
        })


@app.route('/openAI', methods=['POST'])
def openAIResponse():
    data = request.json
    prompt = data["prompt"]

    response = openAI(prompt)

    return jsonify({
        "response": response
    })


## app.run(host=HOSTNAME, port=PORT, debug=True)
if __name__ == "__main__":
    app.run(debug=True)
