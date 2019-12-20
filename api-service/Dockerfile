FROM python:3

COPY ./* /app
WORKDIR /app

RUN apt-get update
RUN pip install -r requirements.txt

CMD python api.py
