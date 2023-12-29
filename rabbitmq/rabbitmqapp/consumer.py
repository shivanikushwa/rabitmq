import pika

class RabbitMQConsumer:
    def __init__(self):
        self.connection = None
        self.channel = None

    def connect(self):
        try:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host='localhost', port=5672, heartbeat=600)
            )
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue='hello')
        except pika.exceptions.AMQPConnectionError as e:
            print(f"Failed to connect to RabbitMQ: {e}")
            # Handle the connection error here
        except Exception as e:
            print(f"An error occurred: {e}")

    def callback(self, ch, method, properties, body):
        print(f" [x] Received {body}")

    def start_consuming(self):
        self.channel.basic_consume(queue='hello', on_message_callback=self.callback, auto_ack=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    def close_connection(self):
        self.connection.close()


consumer = RabbitMQConsumer()
consumer.connect()
consumer.start_consuming()
