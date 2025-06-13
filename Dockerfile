FROM python:3.12-slim

RUN apt-get update && apt-get upgrade -y

RUN mkdir /app

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --upgrade pip && pip install -r requirements.txt

COPY ./src ./src

EXPOSE 8080

CMD ["python", "src/manage.py", "runserver", "0.0.0.0:8080"]
