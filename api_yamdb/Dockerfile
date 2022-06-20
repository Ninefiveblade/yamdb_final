FROM python:3.7-slim
COPY . ./app
RUN pip3 install -r /app/requirements.txt --no-cache-dir
WORKDIR /app/infra_project
LABEL author="Alexeev Ivan"