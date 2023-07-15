FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y git 

COPY requirements.txt ./
COPY bot/ ./

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
