# ML Client with Speech Transcription and Conversation Bot

[![ML Client Build and Test](https://github.com/software-students-fall2022/final-project-team-7/actions/workflows/ml-client.yml/badge.svg)](https://github.com/software-students-fall2022/final-project-team-7/actions/workflows/ml-client.yml)

This ML client allows users to input speech and receive transcription using the wav2vec2 model, and engage in conversation with a chatbot using the text-davinci-003 model.

## Prerequisites

Before using this ML client, make sure you have the following dependencies installed:
* All the dependencies within requirements.txt in ml-client directory
* Facebook's wav2vec2 model (API required)
* OpenAI's text-davinci-003 model (API required)

### Using Command:
    
    pip3 install -r requirements.txt

### Usage:

To use python files seperately:

    from converOpenAI import openAI
    from processSpeech import transcribe


The client will prompt you to input speech file path (take file path + path name as paramter), which will then be transcribed using the wav2vec2 model. You can then engage in conversation with the chatbot using the text-davinci-003 model (take in user prompt as parameter to generate response)

To build and run container using Dockerfile:

    docker build -t <dockerhub username>/final-project-team-7-ml-client .
    docker run -ti --rm -p 5001:5001 <dockerhub username>/final-project-team-7-ml-client:latest

## Credits

This ML client was built using Facebook's wav2vec2 model and OpenAI's text-davinci-003 model. We are grateful to the authors and contributors of these models for making them available for use.

