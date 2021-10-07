import logging, os
from typing import Union
from confluent_kafka import KafkaError
from confluent_kafka.avro import AvroConsumer
from concurrent.futures import ThreadPoolExecutor
from websites_metrics_consumer.classes.EventsHandler import EventHandler

logger = logging.getLogger()
logging.basicConfig(
    format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO
)
logger.setLevel(os.environ.get("logging_level", logging.INFO))


class MetricsConsumer:
    """
    Class that manages the incoming message from the configured Kafka topic.

    """

    def __init__(self, consumer_topic: list, consumer_conf: dict, persistence_conf: Union[dict, str]
                 ):
        self.event_handler = EventHandler(connection_params=persistence_conf)
        self.consumer_topic = consumer_topic
        self.consumer = AvroConsumer(consumer_conf)
        logging.getLogger('urllib3.connectionpool').setLevel(logging.INFO)
        self.executor = ThreadPoolExecutor(max_workers=os.environ.get('max_workers', 5))

    def run(self):
        """
        This method listens to message to consume.
        :return:
        """
        logger.info('The consumer is listening to the topic(s) %s \n' % self.consumer_topic)

        try:
            self.consumer.subscribe(self.consumer_topic, on_assign=self.print_assignment)

            while True:
                incoming_message = self.consumer.poll(1)
                if incoming_message is None:
                    continue
                if incoming_message.error():
                    if incoming_message.error().code() == KafkaError._PARTITION_EOF:
                        # End of partition event
                        logger.error('%s [%d] reached end at offset %d\n' %
                                     (incoming_message.topic(), incoming_message.partition(),
                                      incoming_message.offset()))
                    elif incoming_message.error():
                        logger.error('Consumer Error %s\n' % incoming_message.error())
                        # We do not break the while loop so as to let the consumer rejoin the group the next time the poll() method will be invoked.
                        continue

                else:
                    logger.info('[Topic:%s][Message:%s] \n' % (
                        str.upper(incoming_message.topic()), incoming_message.value()))
                    self.executor.submit(self.event_handler.store_event, incoming_message.value())

        except Exception as whatever_it_is:
            logger.error('EXCEPTION %s on the consumer for topic(s) %s\n' % (
                whatever_it_is, self.consumer_topic))
            pass

        finally:
            logger.error(
                'CLOSING consumer %s with topic(s): %s\n' % (
                    self.consumer, self.consumer_topic))
            self.consumer.close()
            return 1

    def print_assignment(self, consumer, partitions):
        """
        This method just prints out the assigned partition for the consumer
        :param consumer:
        :param partitions:
        :return:
        """
        logger.info(f' {consumer} - {self.consumer_topic} - {partitions}')
