# in Docker, it is common to base a new image on a previously-created image
FROM python:3.8-slim-buster
COPY requirements.txt .
COPY . .
RUN pip3 install -r requirements.txt
ENV FLASK_APP app.py
EXPOSE 5001
CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]