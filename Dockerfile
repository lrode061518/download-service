FROM ubuntu14:std

RUN apt-get update && apt-get install -y python-flask && apt-get clean

EXPOSE 8080

ENTRYPOINT rm /download/* && python provide_download.py && /bin/bash
