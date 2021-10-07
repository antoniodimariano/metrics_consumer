from setuptools import setup, find_packages
from codecs import open

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='websites_metrics_consumer_beta',
    version='1.0.1',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=["psycopg2==2.9.1","confluent_kafka==1.7.0"],
    url='',
    license='',
    python_requires='>=3.6',
    author='Antonio Di Mariano',
    author_email='antonio.dimariano@gmail.com',
    description='An application that consumes metrics from Kafka messages and store the results into ta postgres db',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
