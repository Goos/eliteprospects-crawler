from amqpy import Message, AbstractConsumer
from lib.parsers.player_parser import PlayerParser
import os
import requests
import json
import logging

logger = logging.getLogger(__name__)

class PlayerRequestConsumer(AbstractConsumer):
  BASE_URL = os.environ.get('ELITEPROSPECTS_URL') + '/player.php'

  def run(self, msg: Message):
    logger.info("Received message for player: %s", msg)
    json_msg = json.loads(msg.body)
    
    try:
      url = self.BASE_URL + '?player=%s' % json_msg['player_id']
      request = requests.get(url)
      parser = PlayerParser(request.text)
      logger.info("Parsing data for player: %s", json_msg)
      parser.run()
    except:
      return self.reject(msg)
    
    self.acknowledge(msg)
  def acknowledge(self, msg: Message):
    msg.ack()

  def reject(self, msg: Message):
    msg.reject(True)
    

