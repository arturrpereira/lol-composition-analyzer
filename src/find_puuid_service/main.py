import os
import requests
from loguru import logger
from libs.rabbitmq_connection.rabbitmq import RabbitMQConnection

USERNAME = os.getenv("RABBITMQ_DEFAULT_USER")
PASSWORD = os.getenv("RABBITMQ_DEFAULT_PASS")
HOST = os.getenv("RABBITMQ_HOST")
API_KEY = "RGAPI-a0a78756-6b7e-43e8-ae42-6938feaa8e73"

conn = RabbitMQConnection(host=HOST, username=USERNAME, password=PASSWORD)

logger.info("Establishing connection...")
conn.connect()

logger.info("Declaring exchange...")
conn.exchange_declare(exchange="analyzer", exchange_type="topic")

logger.info("Declaring queue...")
conn.queue_declare(queue_name="teste_puuid")

# summoner_id = 'kzEBew1j0rQa2UY_vE5A5aOeRHuxAuyAHYgQOqG4PGq8XOo'


def get_puuid_request(summoner_id):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://developer.riotgames.com",
    }

    response = requests.get(
        f"https://br1.api.riotgames.com/lol/summoner/v4/summoners/{summoner_id}?api_key={API_KEY}",
        headers=headers,
    )

    if response.ok:
        data = response.json()
        return data["puuid"]


def process_message(summoner_id):
    puuid = get_puuid_request(summoner_id)
    logger.info(f"{puuid} finded!")
    if puuid:
        routing_key = f"puuid.{puuid}"
        conn.message_publisher(
            exchange="analyzer", queue_name=routing_key, message=puuid
        )
        logger.info(f"[X] Message > {puuid} < sent! | routing key > {routing_key} <")


def callback(ch, method, properties, body):
    summoner_id = body.decode()
    process_message(summoner_id)


def main():
    logger.info("Starting consuming....")
    conn.message_consumer(callback=callback, queue_name="teste_puuid")


if __name__ == "__main__":
    main()
