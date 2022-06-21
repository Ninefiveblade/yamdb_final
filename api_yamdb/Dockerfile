FROM python:3.7-slim
COPY . ./app
COPY ./templates ./app/api_yamdb
WORKDIR /app/api_yamdb
RUN pip3 install -r requirements.txt --no-cache-dir
LABEL author="Alexeev Ivan"