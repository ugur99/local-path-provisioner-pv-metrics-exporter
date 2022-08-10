FROM python:3.7
WORKDIR /app
COPY src/deployment/requirements.txt src/deployment/requirements.txt
RUN apt-get update \
    && apt-get upgrade -y \
    && pip3 install -r requirements.txt
#RUN pip3 install -r requirements.txt
COPY . .
CMD [ "python3", "/app/get-pvc.py"]
