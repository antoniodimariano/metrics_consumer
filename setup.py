from setuptools import setup, find_packages
from codecs import open

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='websites_metrics_consumer',
    version='0.0.2',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=["psycopg2","confluent_kafka","avro-python3","requests"],
    url='https://github.com/antoniodimariano/metrics_consumer',
    license='Apache 2.0',
    python_requires='>=3.6',
    author='Antonio Di Mariano',
    author_email='antonio.dimariano@gmail.com',
    description='An application that consumes metrics from Kafka messages and store the results into ta postgres db',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ]
)
