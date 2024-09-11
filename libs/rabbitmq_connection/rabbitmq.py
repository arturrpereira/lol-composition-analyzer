import json
import pika


class RabbitMQConnection:
    def __init__(self, host, port=5672, username="guest", password="guest"):
        self.credentials = pika.PlainCredentials(username=username, password=password)
        self.connection_params = pika.ConnectionParameters(
            host=host, port=port, credentials=self.credentials
        )
        self.connection = None
        self.channel = None

    def connect(self):
        if not self.connection or self.connection.is_closed:
            self.connection = pika.BlockingConnection(self.connection_params)
            self.channel = self.connection.channel()
        return self.channel

    def queue_declare(self, queue_name=""):
        if self.channel:
            result = self.channel.queue_declare(
                queue=queue_name,
                durable=True if queue_name else False,
                exclusive=False if queue_name else True,
                auto_delete=False if queue_name else True,
            )
            return result
        else:
            raise ConnectionError("channel is not open")

    def exchange_declare(self, exchange, exchange_type):
        if self.channel:
            self.channel.exchange_declare(
                exchange=exchange,
                exchange_type=exchange_type,
            )
        else:
            raise ConnectionError("channel is not open")

    def message_publisher(self, message, exchange="", queue_name=""):
        if not self.channel or self.channel.is_closed:
            raise ConnectionError("Channel is not open. Call connect() first.")

        if not isinstance(message, str):
            message = json.dumps(message)

        self.channel.basic_publish(
            exchange=exchange,
            routing_key=queue_name,
            body=message,
            properties=pika.BasicProperties(delivery_mode=2),
        )

    def message_consumer(self, callback, queue_name=""):
        if not self.channel or self.channel.is_closed:
            raise ConnectionError("Channel is not open. Call connect() first.")

        def func_callback(ch, method, properties, body):
            message = body.decode()
            callback(message)
            ch.basic_ack(delivery_tag=method.delivery_tag)

        self.channel.basic_consume(queue=queue_name, on_message_callback=func_callback)
        self.channel.start_consuming()

    def close_connection(self):
        if self.connection and not self.connection.is_closed:
            self.connection.close()
