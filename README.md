[![CircleCI](https://circleci.com/gh/antoniodimariano/metrics_consumer/tree/master.svg?style=svg&circle-token=f7da2eeb3c4a1dbbe2705fda45fdffe02e8ef1ce)](https://circleci.com/gh/antoniodimariano/metrics_consumer/tree/master)
[![codecov](https://codecov.io/gh/antoniodimariano/metrics_consumer/branch/codecoverage/graph/badge.svg?token=G6OQ1T115F)](https://codecov.io/gh/antoniodimariano/metrics_consumer)
![PyPI - License](https://img.shields.io/pypi/l/websites-metrics-consumer)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/websites-metrics-consumer)

# Websites Metrics Consumer

#### Author: Antonio Di Mariano - antonio.dimariano@gmail.com
8a8a7146-c00c-47f2-84fb-b544564c9ec1
## Description

This service is part of the Websites Monitoring Application, a small distributed application 
that aims to produce and collect metrics about the availability of one or more websites. 
This service is responsible for consuming messages about metrics being produced to an Apache Kafka Avro Topic by a different service.
The main action of this service is to store the incoming message into a PostgreSQL database.


## Overview of the Websites Monitoring Application

The application is made of three services that can run in different systems.

There are main two services. 

The first one https://github.com/antoniodimariano/websites_metrics_collector is responsible for fetching and collecting the information from a list of URLs. The information collected is

HTTP Status returned HTTP response time regexp pattern that is expected to be found on the HTML content.
For each record, a message is produced to an Apache Kafka Topic. This service exposes a REST API Service with a POST method to accept a list of URLs to fetch and process.

The second service is https://github.com/antoniodimariano/metrics_consumer that is responsible for consuming messages about metrics being produced to an Apache Kafka Avro Topic by a different service. The main action of this service is to store the incoming message into a PostgreSQL database.

The last one is a Celery Beat based service https://github.com/antoniodimariano/crontab_request that periodically send a POST request with a list of URLS to the `websites_metrics_collector`

So, to run all the whole application,  you don't need to clone the three repos,  You can use these two public python packages

1. https://pypi.org/project/websites-metrics-consumer/ 
2. https://pypi.org/project/websites-metrics-collector/

Create two `python` applications. One will consume messages 

`pip3 install websites-metrics-consumer`

The other will produce metrics 

`pip3 install websites-metrics-collector`

In order to produce metrics, the https://github.com/antoniodimariano/websites_metrics_collector runs a REST Server with a `POST` `/api/v1/websites_metrics` endpoint that accepts a list of URLs to fetch. 
For the complete documentation go here https://github.com/antoniodimariano/websites_metrics_collector/blob/master/README.md

The last application (https://github.com/antoniodimariano/crontab_request) uses Celery Beat to periodically run the task of reading a list or URLs from a local `json` file and will send it to as payload.
of the `POST` request to `/api/v1/websites_metrics`
It requires `Redis` as broker.

You can decide not to use https://github.com/antoniodimariano/crontab_request and implements your own way of requesting a list or URLs to monitor. 
As long as you send a POST Request to the endpoint `/api/v1/websites_metrics` metrics will be collected, messages will be produced and data will be stored. 
I decided to use Celery and not, for instance, a simple timer implemented with Thread or 3-party libs because Celery is robust, scalable and production ready.
I know it comes at the price of having a broker, but I prefer to pay a small price for a significant advance. Not to mention, I am a big fan of Celery!


# How to Run this service

If you want to run from the source code, go to the directory `websites_metrics_consumer` and run `python main`

If you want to use it as package (suggested method) install  `pip3 install websites_metrics_consumer`

Then

1. Set the ENV variables as show in this README.md
2. Then use it this way

```python
def consume_message():
    from websites_metrics_consumer.main import start_consumer
    start_consumer()
    


```

# Requirements

* Python >=3.8


# Dependencies

* confluent_kafka==1.7.0
* psycopg2==2.9.1

# Run test

**NOTE**: for simplicity I am assuming you have a running local instance of PostgreSQL with the following information

* database='test'
* user='postgresql'
* password='test123'
* host='localhost'

`python -m unittest tests/test_db_operations.py`
`python -m unittest test/test_events_handler_class.py`


# Service ENV configuration 

If you are using a Broker that uses `SSL`, like Aiven.com, you need to download the following certificates files and copy them to a folder
 * Access Key
 * Access Certificate
 * CA Certificate

for more information about SSL and Kafka please read https://docs.confluent.io/3.0.0/kafka/ssl.html


Example of your project folder 

```text
myprojectname/
|------configuration/
            __init__.py
            ca.pem
            service.cert
            service.key
|------venv
|main.py
|requirements.txt            

```

| ENV Variable  | VALUE | DESCRIPTION                                                                       |
|---------------|------|------------------------------------------------------------------------------------|
| brokers    | string   | Required. The FQDN of the Apache Kafka Brokers.|
| schema_registry    | string   | Required. The FQDN of the Service Registry.|
| ssl_ca_location    | string   | Required. he relative path to your ca.pem|
| ssl_certificate_location    | string   | Required. The relative path to your service.cert|
| ssl_key_location    | string   | Required. The relative path to your service.key |
| security_protocol    | string   | Required. SSL.|
| persistence_conf    | string   | Required. The full string for connecting to your PostgreSQL database.|
| group_id    | string   | Optional. The consumer group id to assign to the consumer(s) . The default value is `metrics_consumer`|
| consumer_topics    | string or list  | Optional. The Kafka Avro Topic where to consume messages from. The defaul value is `websites_metrics` |
| logging_level    | string   | Optional. The level of logging to use for the built-in `logging` package. The default is `logging.INFO`  |


**Example of mandatory ENV variables to use** 

* brokers=kafka-xxx-yyy-abc.com:12026
* schema_registry=https://user:password@kafka-xxx-yyy-abc.com:12029
* ssl_ca_location=configuration/ca.pem
* ssl_certificate_location=configuration/service.cert
* ssl_key_location=configuration/service.key
* security_protocol=SSL
* persistence_conf=postgres://user:password@mydbhost.com:12024/metrics?sslmode=require



If your broker requires SASL authentication, like Confluent Cloud, these are the ENV variables to include

| ENV Variable  | VALUE | DESCRIPTION                                                                       |
|---------------|------|------------------------------------------------------------------------------------|
| brokers    | string   | Required. The FQDN of the Apache Kafka Brokers.|
| schema_registry    | string   | Required. The FQDN of the Service Registry.|
| sasl_username    | string   | Required. YOUR USERNAME HERE|
| sasl_password    | string   | Required. YOUR PASSWORD HERE|
| schema_registry_basic_auth_user_info    | string   | Required. AUTH HERE |
| schema_registry_basic_auth_credentials_source    | string   | Required. USER_INFO.|
| sasl_mechanisms    | string   | Required. PLAIN.|
| security_protocol    | string   | Required. SASL_SSL.|
| persistence_conf    | string   | Required. The full string for connecting to your PostgreSQL database.|
| group_id    | string   | Optional. The consumer group id to assign to the consumer(s) . The default value is `metrics_consumer`|
| consumer_topics    | string or list  | Optional. The Kafka Avro Topic where to consume messages from. The defaul value is `websites_metrics` |
| logging_level    | string   | Optional. The level of logging to use for the built-in `logging` package. The default is `logging.INFO`  |
