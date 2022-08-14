FROM python:3.7.13-alpine3.16
WORKDIR /app
COPY requirements.txt requirements.txt
RUN apk update \
    && apk upgrade \
    && pip3 install -r requirements.txt
COPY . .
CMD [ "python3", "/app/job.py"]
