FROM python:3.7
LABEL maintainer = "Secam <Secam-s@yandex.ru>"
RUN apt-get update
RUN mkdir /app
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000