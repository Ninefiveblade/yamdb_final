FROM python:3.7-slim
COPY . ./app
WORKDIR /app/infra_project
RUN pip3 install -r /app/requirements.txt --no-cache-dir
LABEL author="Alexeev Ivan"