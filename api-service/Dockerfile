FROM python:3

COPY ./* /app/
WORKDIR /app

RUN apt-get update
RUN pip install -r /app/requirements.txt

CMD python api.py > /data/log_api_service.txt 2>/data/error_log_api_service.txt
