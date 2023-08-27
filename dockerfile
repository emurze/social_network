FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONNUNBUFFERED 1

WORKDIR /service/

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY src src

EXPOSE 8080
