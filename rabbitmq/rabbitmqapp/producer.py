import json
import pika
from django.conf import settings

class RabbitMQProducer:
    def __init__(self):
        try:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host='localhost', port=5672, heartbeat=600)
            )
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue='hello')

        except pika.exceptions.AMQPConnectionError as e:
            print(f"Failed to connect to RabbitMQ: {e}")

    def publish_message(self, message):
        try:
            self.channel.basic_publish(
                exchange='',
                routing_key='hello',
                body=json.dumps(message)
            )
            print(" [x] Sent message:", message)
        except Exception as e:
            print(f"Failed to publish message: {e}")

    def close_connection(self):
        self.connection.close()


# Example usage:
producer = RabbitMQProducer()
# No explicit connect method as the connection is established in __init__()

message_to_publish = {' ': 'value'}  # Your message to be published
producer.publish_message(message_to_publish)

producer.close_connection()
