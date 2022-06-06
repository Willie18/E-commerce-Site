FROM python:3.8

ENV PYTHONUNBUFFERED 1

WORKDIR /app

ADD . /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

RUN python manage.py makemigrations

RUN python manage.py migrate 

RUN echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@myproject.com', 'password')" | python manage.py shell

RUN python manage.py seed

COPY . /app

CMD gunicorn DjangoSite1.wsgi:application --bind 0.0.0.0:$PORT


