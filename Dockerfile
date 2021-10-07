FROM python:3.8
WORKDIR /source_code
ENV PYTHONPATH source_code
RUN git clone https://github.com/edenhill/librdkafka.git
RUN cd librdkafka && ./configure --prefix /usr && make &&  make install
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . /source_code
CMD ["python","main.py"]