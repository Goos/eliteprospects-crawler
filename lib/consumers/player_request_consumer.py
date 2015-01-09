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

  def run(self, msg: Message):
    json_msg = json.loads(msg.body)
    logger.info("Handling message to fetch player: %s", json_msg)
    
    try:
      url = self.BASE_URL + '?player=%s' % json_msg['player_id']
      request = requests.get(url)
      parser = PlayerParser(request.text)
      logger.info("Parsing data for player: %s", json_msg)
      parser.run()
    except(requests.exceptions.RequestException):
      return self.reject(msg, requeue=True)
    except Exception as exc:
      logger.error("Received error when handling message: %s:", json_msg)
      logger.error("%s", traceback.format_exc())
      return self.reject(msg, requeue=False)
    
    self.acknowledge(msg)
  def acknowledge(self, msg: Message):
    msg.ack()

  def reject(self, msg: Message, requeue=False):
    msg.reject(requeue)
    

