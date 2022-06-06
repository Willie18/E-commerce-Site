FROM python:3.8

ENV PYTHONUNBUFFERED 1

WORKDIR /app

ADD . /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

RUN python manage.py makemigrations

RUN python manage.py migrate

RUN python manage.py seed

COPY . /app

CMD gunicorn DjangoSite1.wsgi:application --bind 0.0.0.0:$PORT


