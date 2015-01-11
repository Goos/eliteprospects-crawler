from amqpy import Connection, Timeout, Message
import json
import os

class Exchange:
  players = 'crawler.player.exchange'
  teams = 'crawler.team.exchange'

class Queue:
  players = 'crawler.player.queue'
  teams = 'crawler.team.queue'

class JsonMessage(Message):
  def __init__(self, data):
      data_str = json.dumps(data)
      Message.__init__(self, data_str)

class CrawlPlayerMessage(JsonMessage):
  def __init__(self, player_id):
    message_data = {'player_id': player_id}
    JsonMessage.__init__(self, message_data)

class CrawlTeamMessage(Message): 
  def __init__(self, team_id):
    message_data = {'team_id': team_id}
    JsonMessage.__init__(self, message_data)
 
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

    # Declaring the exchanges and queues on which the messages will be placed.
    self.chan.exchange_declare(Exchange.players, 'direct')
    self.chan.queue_declare(Queue.players)
    self.chan.queue_bind(Queue.players, exchange=Exchange.players, routing_key='crawler')

    self.chan.exchange_declare(Exchange.teams, 'direct')
    self.chan.queue_declare(Queue.teams)
    self.chan.queue_bind(Queue.teams, exchange=Exchange.teams, routing_key='crawler')


  def close(self):
    self.conn.close()

  def drain(self, timeout=None):
    self.conn.drain_events(timeout)

  def publish(self, message: JsonMessage):
    if isinstance(message, CrawlPlayerMessage):
      self.chan.basic_publish(message, exchange=Exchange.players, routing_key='crawler')
    elif isinstance(message, CrawlTeamMessage):
      self.chan.basic_publish(message, exchange=Exchange.teams, routing_key='crawler')

  def purge(self):
    self.chan.queue_purge(Queue.players)
    self.chan.queue_purge(Queue.teams)
  
