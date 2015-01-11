import os, signal, sys
import logging
import json
from src.amqp_client import AMQPClient, Queue
from src.consumers.player_request_consumer import PlayerRequestConsumer
from src.database import Player, DBClient

def main():  
  # Configuring the logging format.
  LOG_FORMAT = '%(levelname) -5s %(asctime) -1s %(name)-0s:%(funcName)-0s:%(lineno) -1s: %(message)s'
  logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
  logger = logging.getLogger(__name__)

  # Setting up the AMQP-client with the default configuration,
  # which is pulling everything from the environment.
  client = AMQPClient()
   
  # Setting up the consumer that waits for messages related to crawling player profiles.
  pl_consumer = PlayerRequestConsumer(client.chan, Queue.players) 
  pl_consumer.declare() 

  terminated = False
  # Adding a handler that closes the amqp-connection when receiving a termination signal.
  def sigterm_handler(signal, frame):
    logger.info('Got SIGTERM, shutting down.')
    terminated = True
    # Deleting the reference to the conumer and closing
    # the AMQP-connection.
    del pl_consumer
    client.close()
  
  signal.signal(signal.SIGTERM, sigterm_handler)

  # Setting up the runloop that waits and drains the events from the queue.
  while not terminated:
    client.drain(timeout=None)

if __name__ == '__main__':
    main()
