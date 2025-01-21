FROM python:3.11-slim

WORKDIR /app

COPY ./src/match-info-consumer /app

COPY ./libs /app/libs

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]