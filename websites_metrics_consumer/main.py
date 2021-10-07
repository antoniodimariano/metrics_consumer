def start_consumer():
    """
    Here the game starts
    :return:
    """
    from websites_metrics_consumer.helpers.confluent_kafka_configuration_builder import \
        build_consumer_configuration_from_os_env_vars
    from websites_metrics_consumer.communication.consumers import MetricsConsumer
    import os
    consumer_topics = [os.environ.get('consumer_topics', 'websites_metrics')]
    persistence_conf = os.environ.get('persistence_conf')
    service_consumer = MetricsConsumer(consumer_conf=
    build_consumer_configuration_from_os_env_vars(
        group_id=os.environ.get('group_id', 'metrics_consumer'), offset=os.environ.get('consumer_offset','latest')),
        consumer_topic=consumer_topics,persistence_conf=persistence_conf)
    service_consumer.run()


if __name__ == '__main__':
    start_consumer()
