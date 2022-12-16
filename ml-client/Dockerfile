# in Docker, it is common to base a new image on a previously-created image
# Use an official Python runtime image as a parent image to base this image on
FROM python:2.7-slim
# Install any needed packages specified in requirements.txt
# in Python, a requirements.txt file is a way of indicating dependencies in a way that the package manager, pip, can understand
RUN pip install --trusted-host pypi.python.org -r requirements.txt
# by default Docker containers are closed off to the external world
# Make port 80 available to the world outside this container
EXPOSE 80
# Run app.py when the container launches
CMD ["python", "__main__.py"]
