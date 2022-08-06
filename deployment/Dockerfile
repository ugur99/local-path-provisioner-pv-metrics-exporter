FROM python:3.7
WORKDIR /app
COPY requirements.txt requirements.txt
RUN apt-get update 
RUN pip3 install -r requirements.txt
COPY . .
CMD [ "python3", "/app/get-pvc.py"]