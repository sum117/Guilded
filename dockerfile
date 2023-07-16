FROM python:3.10-slim-buster

WORKDIR /app

RUN apt-get update && apt-get install -y git 

COPY requirements.txt ./
COPY bot/ ./

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
