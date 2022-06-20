FROM python:3.7-slim
COPY . ./app
COPY requirements.txt /app
RUN pip3 install -r /app/requirements.txt --no-cache-dir
LABEL author="Alexeev Ivan"