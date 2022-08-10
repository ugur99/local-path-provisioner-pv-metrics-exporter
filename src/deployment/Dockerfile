FROM python:3.7
WORKDIR /app
COPY src/deployment/requirements.txt requirements.txt
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get upgrade libgnutls30 -y \
    && apt-get install -y --no-install-recommends 
RUN pip3 install -r requirements.txt
COPY . .
CMD [ "python3", "/app/get-pvc.py"]
