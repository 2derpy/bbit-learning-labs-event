import pika
import os
from tech_lab_on_campus.market_watch.producer_and_consumer.consumer.consumer_interface import mqConsumerInterface

class mqConsumer(mqConsumerInterface):
    def __init__(self, binding_key: str, exchange_name: str, queue_name: str) -> None:
        self.binding_key = binding_key
        self.exchange_name = exchange_name
        self.queue_name = queue_name

        self.setupRMQConnection()

    def setupRMQConnection(self) -> None:
        # Set-up Connection to RabbitMQ service
        self.parameters = pika.ConnectionParameters("localhost")
        self.connection = pika.BlockingConnection(self.parameters)

        # Establish Channel
        self.channel = self.connection.channel()

        # Create Queue if not already present
        if self.queue_name:
            self.channel.queue_declare(queue=self.queue_name)

        # Create the exchange if not already present
        if self.exchange_name:
            self.channel.exchange_declare(
                exchange=self.exchange_name, exchange_type="topic"
            )

        # Bind Binding Key to Queue on the exchange
        if self.exchange_name and self.queue_name and self.binding_key:
            self.channel.queue_bind(
                exchange=self.exchange_name,
                queue=self.queue_name,
                routing_key=self.binding_key,
            )

        # Set-up Callback function for receiving messages
        self.channel.basic_consume(
            queue=self.queue_name, on_message_callback=self.on_message_callback
        )

    def on_message_callback(self, channel, method_frame, header_frame, body) -> None:
        # Acknowledge message
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)

        # Print message (The message is contained in the body parameter variable)
        print(f"Received message: {body.decode()}")

        # Close the connection
        self.channel.close()
        self.connection.close()

    def startConsuming(self) -> None:
        # Start consuming messages
        print(" [*] Waiting for messages. To exit press CTRL+C")
        self.channel.start_consuming()

    def __del__(self) -> None:
        # Print "Closing RMQ connection on destruction"
        print("Closing RMQ connection on destruction")

        try:
            # Close Channel and Connection if they are still open
            if self.channel and self.channel.is_open:
                self.channel.close()
            if self.connection and self.connection.is_open:
                self.connection.close()
        except Exception:
            pass
