from amqpy import Message, AbstractConsumer
from lib.parsers.player_parser import PlayerParser
import os
import requests
import json
import logging
import traceback

logger = logging.getLogger(__name__)

class PlayerRequestConsumer(AbstractConsumer):
  BASE_URL = os.environ.get('ELITEPROSPECTS_URL') + '/player.php'

  # Method called when handling a message.
  def run(self, msg: Message):    
    try:
      # Assuming messages are sent as JSON. If not, an exception 
      # will be raised and the message will be dropped.
      json_msg = json.loads(msg.body)
      logger.info("Handling message to fetch player: %s", json_msg)

      # Fetching the page for the player in questiom pulling 
      # out the player-id from the message.
      url = self.BASE_URL + '?player=%s' % json_msg['player_id']
      logger.info("Loading data for player: %s", url)
      request = requests.request('get', url)

      # Instantiating a parser with the HTML blob.
      parser = PlayerParser(request.text)
      logger.info("Parsing data for player: %s", json_msg)

      # The parser's `run`-method will extract the data and 
      # return a dictionary. 
      parsed_data = parser.run()
      logger.info(parsed_data)

    # In case of HTTP-related exceptions, reject the message,
    # but requeue it, as it's probably temporary.
    except(requests.exceptions.RequestException):
      return self.reject(msg, requeue=True)
    # In case of generic exceptions, simply log the error and
    # reject the message, as it was probably our fault.
    except:
      logger.error("Received error when handling message: %s:", json_msg)
      logger.error("%s", traceback.format_exc())
      return self.reject(msg, requeue=False)
    
    # Finally acknowledge the message, removing it from the queue.
    self.acknowledge(msg)

  def acknowledge(self, msg: Message):
    msg.ack()

  def reject(self, msg: Message, requeue=False):
    msg.reject(requeue)
    

