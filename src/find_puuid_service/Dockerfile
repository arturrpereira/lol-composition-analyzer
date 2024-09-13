FROM python:3.10

WORKDIR /app

COPY ./src/find_puuid_service /app

COPY ./libs /app/libs

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
