import os
import sys
from pathlib import Path


def build_consumer_configuration_from_os_env_vars(group_id: str, offset: str = 'latest') -> dict:
    """
    This method builds the configuration for initializing the AVRO Confluent Producer. It parses each entry in kwargs
    and add each key/value to the producer_conf dict by replacing any occurrence of "_" with "."

    :param offset:
    :param group_id:
    :param topic:
    :return:
    """
    configuration_from_env = {
        'brokers_uri': os.environ.get('brokers'),
        'schema_registry_url': os.environ.get('schema_registry'),
        'group_id': group_id,
        'security_protocol': os.environ.get('security_protocol'),
        'ssl_ca_location': os.environ.get('ssl_ca_location'),
        'ssl_certificate_location': os.environ.get('ssl_certificate_location'),
        'ssl_key_location': os.environ.get('ssl_key_location'),
        'basic_auth_credentials_source': os.environ.get('basic_auth_credentials_source'),
        'sasl_mechanisms': os.environ.get('sasl_mechanisms'),
        'debug': os.environ.get('debug', 0),
        'api_version_request': os.environ.get('api_version_request', 1)
    }

    configuration_from_env['bootstrap_servers'] = configuration_from_env.get('brokers_uri')
    consumer_conf = {
        'enable.auto.commit': 'true',
        'group.id': group_id,
        'default.topic.config': {'auto.offset.reset': offset}}

    if configuration_from_env.get('basic_auth_credentials_source'):
        consumer_conf['schema.registry.basic.auth.credentials.source'] = configuration_from_env.get(
            'basic_auth_credentials_source')
    if configuration_from_env.get('basic_auth_user_info'):
        consumer_conf['schema.registry.basic.auth.user.info'] = configuration_from_env.get('basic_auth_user_info')
    # removing what it's not needed as consumers' config
    configuration_from_env.pop('brokers_uri', '')
    configuration_from_env.pop('basic_auth_credentials_source', '')
    configuration_from_env.pop('basic_auth_user_info', '')

    # translating all the keys replacing the _ with . as requested
    for entry in configuration_from_env:
        if configuration_from_env.get(entry):
            consumer_conf[entry.replace('_', '.')] = configuration_from_env.get(entry)

    if 'ssl.ca.location' not in consumer_conf:
        # here we are sure that the default certificate will be used
        cacert_path = Path(__file__).parent / "../std_ssl_cert/cacert.pem"

        consumer_conf['ssl.ca.location'] = cacert_path
    elif 'ssl.ca.location' in consumer_conf:
        consumer_conf['ssl.ca.location'] = os.path.abspath(consumer_conf.get('ssl.ca.location'))
    if 'ssl.certificate.location' in consumer_conf:
        consumer_conf['ssl.certificate.location'] = os.path.abspath(consumer_conf.get('ssl.certificate.location'))
    if 'ssl.key.location' in consumer_conf:
        consumer_conf['ssl.key.location'] = os.path.abspath(consumer_conf.get('ssl.key.location'))

    if 'security.protocol' not in consumer_conf:
        consumer_conf['security.protocol'] = 'plaintext'
    if configuration_from_env.get('debug') and int(configuration_from_env.get('debug')):
        consumer_conf["debug"] = "cgrp"
    if not int(configuration_from_env.get('api_version_request', 1)):
        # this is for brokers <= 0.10
        consumer_conf['api.version.request'] = 'false'
        consumer_conf['broker.version.fallback'] = '0.9.0.1'

    sys.stderr.write('[Consumer Conf]:  %s\n' % consumer_conf)

    return consumer_conf
