FROM python:3.7-slim
COPY ./requirements.txt /app
COPY . ./app
WORKDIR /app
RUN pip3 install -r /app/requirements.txt --no-cache-dir
LABEL author="Alexeev Ivan"