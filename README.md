[![ML Client Build and Test](https://github.com/software-students-fall2022/final-project-team-7/actions/workflows/ml-client.yml/badge.svg)](https://github.com/software-students-fall2022/final-project-team-7/actions/workflows/ml-client.yml)
[![Web App Build and Test](https://github.com/software-students-fall2022/final-project-team-7/actions/workflows/web-app.yml/badge.svg)](https://github.com/software-students-fall2022/final-project-team-7/actions/workflows/web-app.yml)

[![Machine Learning Client Docker Image CICD](https://github.com/software-students-fall2022/final-project-team-7/actions/workflows/ml-docker-image.yml/badge.svg)](https://github.com/software-students-fall2022/final-project-team-7/actions/workflows/ml-docker-image.yml)
[![Web App Client Docker Image CICD](https://github.com/software-students-fall2022/final-project-team-7/actions/workflows/web-app-client.yml/badge.svg)](https://github.com/software-students-fall2022/final-project-team-7/actions/workflows/web-app-client.yml)

[![Continuous Deployment](https://github.com/software-students-fall2022/final-project-team-7/actions/workflows/deploy.yml/badge.svg)](https://github.com/software-students-fall2022/final-project-team-7/actions/workflows/deploy.yml)
# Final Project

This web app allows user to have a converation with a bot using only voice prompt. The chatroom will transcribe user's speech and respond to it as a normal conversation. [Check it out here](http://104.131.177.209/)

Table of contents
=================
* [DockerHub Links](#dockerhub-links)
* [Team Members](#team-members)
* [Configuration](#configuration)
* [Usage](#usage)

## DockerHub Links

There are two containers built in this project. One for back-end routers that access all the machine learning functionalities including voice transcribe and chat bot, hosted on port 5001. One for front-end web page, hosted on port 5000.

The Links to Container Images Hosted on GitHub:

final-project-team-7-ml-client: https://hub.docker.com/r/yvonne511/final-project-team-7-web-app-client


final-project-team-7-web-app-client: https://hub.docker.com/r/yvonne511/final-project-team-7-web-app-client

## Team Members
[Yvonne Wu (Yiyi Wu)](https://github.com/Yvonne511)

[Larry Li](https://github.com/86larryli)

[Winston Zhang](https://github.com/Midas0231)

[Evan Huang](https://github.com/EV9H)

[Harvey Dong](https://github.com/junyid)

[Otis Lu](https://github.com/OtisL99)

## Configuration

### To run the machine learning client:

1. Goes to ml-client folder, install all dependencies

        pip3 install -r requirements.txt

2. Build container by running following command:

        docker build -t <dockerhub username>/final-project-team-7-ml-client .

3. Run container images on port 5001 by the following command:

        docker run -ti --rm -p 5001:5001 <dockerhub username>/final-project-team-7-ml-client:latest

### To run the web app client:

1. Goes to ml-client folder, install all dependencies

        pip3 install -r requirements.txt

2. Build container by running following command:

        docker build -t <dockerhub username>/final-project-team-7-web-app-client .

3. Run container images on port 5000 by the following command:

        docker run -ti --rm -p 5001:5001 <dockerhub username>/final-project-team-7-web-app-client:latest

### To run test:

Goes to each repository and run:

    pytest

## Usage

- User can login
    - User can see its own profile
- User can speak to a chatbot
- User can check the chat history


