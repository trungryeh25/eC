 # Pull base image
FROM python:3.11

# Set environmental variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work dicrectory
WORKDIR /code

# Install dependencies
COPY Pipfile Pipfile.lock requirements.txt /code/
RUN pip3 install pipenv && pipenv install --system && pip3 install -r requirements.txt

# Copy project
COPY eCommerce/.env /code/
COPY . /code/