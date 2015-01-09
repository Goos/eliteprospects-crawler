import os, signal, sys
import logging
import json
from amqpy import Connection, Timeout, Message
from lib.consumers.player_request_consumer import PlayerRequestConsumer

def main():  
  LOG_FORMAT = '%(levelname) -5s %(asctime) -1s %(name)-0s:%(funcName)-0s:%(lineno) -1s: %(message)s'
  logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
  logger = logging.getLogger(__name__)
  
  host = os.environ.get('CLOUDAMQP_RABBITMQ_AMQP_HOST')
  vhost = os.environ.get('CLOUDAMQP_RABBITMQ_AMQP_VIRTUALHOST')
  login = os.environ.get('CLOUDAMQP_RABBITMQ_AMQP_LOGIN')
  password = os.environ.get('CLOUDAMQP_RABBITMQ_AMQP_PASSWORD')
  port = os.environ.get('CLOUDAMQP_RABBITMQ_AMQP_PORT')
  url = os.environ.get('CLOUDAMQP_RABBITMQ_AMQP_URL')

  conn = Connection(host=host, port=port, userid=login, password=password, virtual_host=vhost)
  chan = conn.channel()

  chan.exchange_declare('crawler.exchange', 'direct')
  chan.queue_declare('crawler.queue')
  chan.queue_bind('crawler.queue', exchange='crawler.exchange', routing_key='crawler')

  msg_body = json.dumps({'player_id': 23047})
  chan.basic_publish(Message(msg_body), exchange='crawler.exchange', routing_key='crawler')
  msg_body = json.dumps({'player_id': 23048})
  chan.basic_publish(Message(msg_body), exchange='crawler.exchange', routing_key='crawler')
  msg_body = json.dumps({'player_id': 23049})
  chan.basic_publish(Message(msg_body), exchange='crawler.exchange', routing_key='crawler')
  msg_body = json.dumps({'player_id': 23050})
  chan.basic_publish(Message(msg_body), exchange='crawler.exchange', routing_key='crawler')
  
  pl_consumer = PlayerRequestConsumer(chan, 'crawler.queue') 
  pl_consumer.declare()

  def sigterm_handler(signal, frame):
    logger.info('Got SIGTERM, shutting down.')
    conn.close()
  
  signal.signal(signal.SIGTERM, sigterm_handler)

  while True:
    conn.drain_events(timeout=None)

if __name__ == '__main__':
    main()
