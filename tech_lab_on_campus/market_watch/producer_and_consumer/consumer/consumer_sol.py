
from consumer_interface import mqConsumerInterface




class mqConsumer(mqConsumerInterface):
    def __init__(
        self, binding_key: str, exchange_name: str, queue_name: str
    ) -> None:
        super().__init__(binding_key, exchange_name, queue_name)

if __name__ == "__main__":
    # Create an instance of the mqConsumer class with appropriate parameters
    consumer = mqConsumer(binding_key="my_binding_key", exchange_name="my_exchange", queue_name="my_queue")

    # Start consuming messages
    consumer.startConsuming()


