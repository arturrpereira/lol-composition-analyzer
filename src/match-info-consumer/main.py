import os
import requests
from loguru import logger
from libs.rabbitmq_connection.rabbitmq import RabbitMQConnection
from pymongo import MongoClient

# RabbitMQ configs
USERNAME = os.getenv("RABBITMQ_DEFAULT_USER")
PASSWORD = os.getenv("RABBITMQ_DEFAULT_PASS")
HOST = os.getenv("RABBITMQ_HOST")

# MongoDB configs
MONGO_USERNAME = os.getenv("MONGO_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")

RIOT_API_KEY = os.getenv("RIOT_API_KEY")

conn = RabbitMQConnection(host=HOST, username=USERNAME, password=PASSWORD)

queue_name = "match_info_consumer"

logger.info("Establishing connection...")
conn.connect()

logger.info("Declaring exchange...")
conn.exchange_declare(exchange="analyzer", exchange_type="direct")

logger.info("Declaring queue...")
conn.queue_declare(queue_name=queue_name)

# Binding Queue
conn.queue_bind(exchange="analyzer", queue=queue_name, routing_key="match")


def get_winner(teams):
    for team in teams:
        if team["win"]:
            return team["teamId"]


def build_teams(participants):
    blue = []
    red = []

    for participant in participants:
        player = {"championName": participant["championName"], "championId": participant["championId"]}

        if participant["teamId"] == 100:
            blue.append(player)
        else:
            red.append(player)

    return blue, red


def save_match_mongodb(data):
    logger.info("Saving data in mongoDb")
    client = MongoClient(f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@mongodb:27017/")

    db = client["lol-analyzer"]
    collection = db["matches"]

    match_info = data["info"]

    blue, red = build_teams(match_info["participants"])

    winner = get_winner(match_info["teams"])

    match = {
        "patch": match_info["gameVersion"],
        "winner_team": winner,
        "blue": blue,
        "red": red,
    }

    collection.insert_one(match)
    logger.info("Data saved successfully!")


def get_match_metadata(match_id):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://developer.riotgames.com",
    }

    response = requests.get(
        f"https://americas.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={RIOT_API_KEY}",
        headers=headers,
    )

    if response.ok:
        logger.info("Match finded")
        return response.json()


def process_message(match_id):
    data = get_match_metadata(match_id)

    if data:
        save_match_mongodb(data)


def callback(ch, method, properties, body):
    match_id = body.decode()
    process_message(match_id)


def main():
    logger.info("Starting consuming...")
    conn.message_consumer(callback=callback, queue_name=queue_name)


if __name__ == "__main__":
    main()

