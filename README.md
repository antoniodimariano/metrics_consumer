[![CircleCI](https://circleci.com/gh/antoniodimariano/metrics_consumer/tree/master.svg?style=svg&circle-token=f7da2eeb3c4a1dbbe2705fda45fdffe02e8ef1ce)](https://circleci.com/gh/antoniodimariano/metrics_consumer/tree/master)
# Websites Metrics Consumer

#### Author: Antonio Di Mariano - antonio.dimariano@gmail.com

## Description

This service is part of the Websites Monitoring Application, a small distributed application 
that aims to produce and collect metrics about the availability of one or more websites. 

This service is responsible for consuming messages about metrics being produced to an Apache Kafka Avro Topic by a different service.
The main action of this service is to store the incoming message into a PostgreSQL database.


# Requirements

* Python >=3.8

# Run

`python main`

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
