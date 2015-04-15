FROM python:3

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app
COPY requirements.txt runserver.py /usr/src/app/
RUN pip install -r requirements.txt

COPY ./server ./server

CMD ["python", "-u", "runserver.py"]

EXPOSE 5000
