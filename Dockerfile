FROM python:3.10

RUN apt-get update

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

WORKDIR /app

COPY . /app

EXPOSE 8000

WORKDIR /app/src

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]