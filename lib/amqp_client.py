from amqpy import Connection, Timeout, Message
from enum import Enum
import json
import os

class MessageType(Enum):
  crawl_player = 1
  crawl_team = 2

class Queue:
  players = 'crawler.player.queue'
  teams = 'crawler.team.queue'

class AMQPClient(object):
  def __init__(self, host=None, vhost=None, login=None, password=None, port=None, url=None):
    # Gathering credentials and the likes from the environment,
    # unless specified.
    self.host = host if host else os.environ.get('CLOUDAMQP_RABBITMQ_AMQP_HOST')
    self.vhost = vhost if vhost else os.environ.get('CLOUDAMQP_RABBITMQ_AMQP_VIRTUALHOST')
    self.login = login if login else os.environ.get('CLOUDAMQP_RABBITMQ_AMQP_LOGIN')
    self.password = password if password else os.environ.get('CLOUDAMQP_RABBITMQ_AMQP_PASSWORD')
    self.port = port if port else os.environ.get('CLOUDAMQP_RABBITMQ_AMQP_PORT')
    self.url = url if url else os.environ.get('CLOUDAMQP_RABBITMQ_AMQP_URL')
    
    # Setting up the amqp-connection to RabbitMQ via amqpy
    self.conn = Connection(host=self.host, port=self.port, userid=self.login, password=self.password, virtual_host=self.vhost)
    self.chan = self.conn.channel()

    # Declaring the exchange and queue on which the messages will be placed.
    self.chan.exchange_declare('crawler.exchange', 'direct')
    self.chan.queue_declare(Queue.players)
    self.chan.queue_bind(Queue.players, exchange='crawler.exchange', routing_key='crawler')

  def close(self):
    self.conn.close()

  def drain(self, timeout=None):
    self.conn.drain_events(timeout)

  def publish(self, message_data, message_type: MessageType):
    data_str = json.dumps(message_data)
    if message_type == MessageType.crawl_player:
      self.chan.basic_publish(Message(data_str), exchange='crawler.exchange', routing_key='crawler')
    elif message_type == MesageType.crawl_team:
      return None
