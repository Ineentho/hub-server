FROM python:3

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/
RUN pip install -r requirements.txt

COPY ./server ./server

CMD ["python", "-u", "./server/server.py"]

EXPOSE 5000
