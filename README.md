[![ML Client Build and Test](https://github.com/software-students-fall2022/final-project-team-7/actions/workflows/ml-client.yml/badge.svg)](https://github.com/software-students-fall2022/final-project-team-7/actions/workflows/ml-client.yml)
[![Web App Build and Test](https://github.com/software-students-fall2022/final-project-team-7/actions/workflows/web-app.yml/badge.svg)](https://github.com/software-students-fall2022/final-project-team-7/actions/workflows/web-app.yml)

[![Machine Learning Client Docker Image CICD](https://github.com/software-students-fall2022/final-project-team-7/actions/workflows/ml-docker-image.yml/badge.svg)](https://github.com/software-students-fall2022/final-project-team-7/actions/workflows/ml-docker-image.yml)
[![Web App Client Docker Image CICD](https://github.com/software-students-fall2022/final-project-team-7/actions/workflows/web-app-client.yml/badge.svg)](https://github.com/software-students-fall2022/final-project-team-7/actions/workflows/web-app-client.yml)

[![Continuous Deployment](https://github.com/software-students-fall2022/final-project-team-7/actions/workflows/deploy.yml/badge.svg)](https://github.com/software-students-fall2022/final-project-team-7/actions/workflows/deploy.yml)

[![ML Client](https://img.shields.io/docker/v/yvonne511/final-project-team-7-ml-client/latest?label=ml-client&logo=docker)](https://hub.docker.com/r/yvonne511/final-project-team-7-ml-client)
[![Web Client](https://img.shields.io/docker/v/yvonne511/final-project-team-7-web-app-client/latest?label=web-client&logo=docker)](https://hub.docker.com/r/yvonne511/final-project-team-7-web-app-client)


# Final Project

This web app allows users to have conversations with a bot using voice prompts. The chatroom will transcribe the user's speech and respond to it as a normal conversation. [Check it out here](http://104.131.177.209/)


## Table of contents

* [DockerHub Links](#dockerhub-links)
* [Team Members](#team-members)
* [Usage](#usage)
    * [Build and Run From Source Code](#build-and-run-from-source-code)


## Team Members

[Yvonne Wu (Yiyi Wu)](https://github.com/Yvonne511)

[Larry Li](https://github.com/86larryli)

[Winston Zhang](https://github.com/Midas0231)

[Evan Huang](https://github.com/EV9H)

[Harvey Dong](https://github.com/junyid)

[Otis Lu](https://github.com/OtisL99)


## DockerHub Links

There are two containers built in this project. One for all the machine learning functionalities, including voice transcribe and chat bot. One for the web app.

The Links to Container Images Hosted on DockerHub:

[yvonne511/final-project-team-7-ml-client](https://hub.docker.com/r/yvonne511/final-project-team-7-ml-client)

[yvonne511/final-project-team-7-web-app-client](https://hub.docker.com/r/yvonne511/final-project-team-7-web-app-client)


## Usage

### Build and Run From Source Code

1. Clone the project source code to your machine:

    ```bash
    git clone https://github.com/software-students-fall2022/final-project-team-7.git
    ```

2. In the project root directory (where `docker-compose.yaml` is), create a `.env` file:

    ```
    WEB_CLIENT_LOCAL_PORT=<YOUR_WEB_CLIENT_LOCAL_PORT>
    FLASK_DEBUG=0

    # WEB CLIENT
    SESSION_KEY=<YOUR_SESSION_KEY>
    MONGO_DBNAME=chatbot
    MONGO_URI=<YOUR_MONGODB_URI>

    # ML CLIENT
    API_TOKEN=<YOUR_HUGGINGFACE_API_KEY>
    OPENAI_API_KEY=<YOUR_OPENAI_API_KEY>
    ```

3. In the project root directory (where `docker-compose.yaml` is), run:

    ```bash
    docker compose up --build
    ```

    The web client will run at `http://localhost:<YOUR_WEB_CLIENT_LOCAL_PORT>`.


### Testing using Pytest

#### Testing Web Client

1. Go to the web client container (make sure the web client container is running first):

    ```
    docker exec -it web-client bash
    ```

2. Run `pytest`:

    ```
    pytest
    ```

#### Testing Machien Learning Client

1. Go to the machine learning client container (make sure the machine learning client container is running first):

    ```
    docker exec -it ml-client bash
    ```

2. Run `pytest`:

    ```
    pytest
    ```