FROM python:3.10

RUN apt-get update

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' ./entrypoint.sh
RUN chmod +x ./entrypoint.sh

WORKDIR /app

COPY . /app

EXPOSE 8000

WORKDIR /app/src

CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]