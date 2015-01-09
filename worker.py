import os, signal, sys
import logging
import json
from amqpy import Connection, Timeout, Message
from lib.consumers.player_request_consumer import PlayerRequestConsumer

def main():  
  # Configuring the logging format.
  LOG_FORMAT = '%(levelname) -5s %(asctime) -1s %(name)-0s:%(funcName)-0s:%(lineno) -1s: %(message)s'
  logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
  logger = logging.getLogger(__name__)
  
  # Gathering credentials and the likes from the environment.
  host = os.environ.get('CLOUDAMQP_RABBITMQ_AMQP_HOST')
  vhost = os.environ.get('CLOUDAMQP_RABBITMQ_AMQP_VIRTUALHOST')
  login = os.environ.get('CLOUDAMQP_RABBITMQ_AMQP_LOGIN')
  password = os.environ.get('CLOUDAMQP_RABBITMQ_AMQP_PASSWORD')
  port = os.environ.get('CLOUDAMQP_RABBITMQ_AMQP_PORT')
  url = os.environ.get('CLOUDAMQP_RABBITMQ_AMQP_URL')

  # Setting up the amqp-connection to RabbitMQ via amqpy
  conn = Connection(host=host, port=port, userid=login, password=password, virtual_host=vhost)
  chan = conn.channel()

  # Declaring the exchange and queue on which the messages will be placed.
  chan.exchange_declare('crawler.exchange', 'direct')
  chan.queue_declare('crawler.queue')
  chan.queue_bind('crawler.queue', exchange='crawler.exchange', routing_key='crawler')
  
  # Setting up the consumer that waits for messages related to crawling player profiles.
  pl_consumer = PlayerRequestConsumer(chan, 'crawler.queue') 
  pl_consumer.declare()

  # Example messages:
  # msg_body = json.dumps({'player_id': 23047})
  # chan.basic_publish(Message(msg_body), exchange='crawler.exchange', routing_key='crawler')
  # msg_body = json.dumps({'player_id': 23048})
  # chan.basic_publish(Message(msg_body), exchange='crawler.exchange', routing_key='crawler')
  # msg_body = json.dumps({'player_id': 23049})
  # chan.basic_publish(Message(msg_body), exchange='crawler.exchange', routing_key='crawler')
  # msg_body = json.dumps({'player_id': 23050})
  # chan.basic_publish(Message(msg_body), exchange='crawler.exchange', routing_key='crawler')

  # Adding a handler that closes the amqp-connection when receiving a termination signal.
  def sigterm_handler(signal, frame):
    logger.info('Got SIGTERM, shutting down.')
    conn.close()
  
  signal.signal(signal.SIGTERM, sigterm_handler)

  # Setting up the runloop that waits and drains the events from the queue.
  while True:
    conn.drain_events(timeout=None)

if __name__ == '__main__':
    main()
