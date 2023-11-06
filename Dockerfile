FROM python:3.11-slim
WORKDIR /app

RUN apt update && apt install pkg-config build-essential

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD [ "python", "manage.py", "runserver", "0.0.0.0:80" ]
