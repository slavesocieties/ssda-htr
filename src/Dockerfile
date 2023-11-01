# Set base image (host OS)
FROM python:3.12-slim

# By default, listen on port 5000
EXPOSE 5000/tcp

# Set the working directory in the container
WORKDIR /service

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install --upgrade setuptools
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --user

# Copy the content of the local src directory to the working directory
COPY ./segmentation .
COPY ./flask_app.py .

# Specify the command to run on container start
CMD [ "python", "flask_app.py" ]