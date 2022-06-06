FROM python:3.8

ENV PYTHONUNBUFFERED 1

WORKDIR /app

ADD . /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

RUN python manage.py seed

COPY . /app

CMD [ "python" ,"manage.py","runserver",$PORT] 
