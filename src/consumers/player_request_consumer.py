import os
import requests
import json
import logging
import traceback
from amqpy import Message, AbstractConsumer
from src.parsers.player_parser import PlayerParser
from src.database import DBClient, Player

logger = logging.getLogger(__name__)

class PlayerRequestConsumer(AbstractConsumer):
  BASE_URL = os.environ.get('ELITEPROSPECTS_URL') + '/player.php'

  def __init__(self, channel, queue, consumer_tag='', no_local=False, no_ack=False, exclusive=False, use_thread=False):
    super(PlayerRequestConsumer, self).__init__(channel, queue, consumer_tag, no_local, no_ack, exclusive, use_thread)
    self.db_client = DBClient() 

  # Method called when handling a message.
  def run(self, msg: Message):    
    try:
      # Assuming messages are sent as JSON. If not, an exception 
      # will be raised and the message will be dropped.
      json_msg = json.loads(msg.body)
      logger.info("Handling message to fetch player: %s", json_msg)
      player_id = json_msg['player_id']

      if self.db_client.player_exists(eliteprospects_id = player_id):
        logger.info("Player with id '%i' already exists.", player_id)
        return self.reject(msg)

      # Fetching the page for the player in question 
      raw_data = self.fetch_player_data(player_id) 
      
      # Parsing the raw data, pulling out the values we want.
      parsed_data = self.parse_player_data(raw_data)
      # Adding the id from the message as the 'eliteprospects_id'.
      parsed_data['eliteprospects_id'] = player_id
      
      # Creating a new player from the parsed data.
      self.create_new_player(parsed_data)
      
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
 
  def fetch_player_data(self, player_id):
    url = self.BASE_URL + '?player=%s' % player_id
    logger.info("Loading data for player at URL: %s", url)
    request = requests.request('get', url)

    return request.text

  def parse_player_data(self, raw_html_blob):
    # Instantiating a parser with the HTML blob.
    parser = PlayerParser(raw_html_blob)
    logger.info("Parsing data for player.")
    # The parser's `run`-method will extract the data and 
    # return a dictionary. 
    return parser.run()

  def create_new_player(self, parsed_player_data):
    # Creating a player model out of the parsed data.
    player = Player(**parsed_player_data) 
    
    # Inserting the player to the database.
    self.db_client.add_player(player)
    logger.info('Added player %s to the database', player)

  def acknowledge(self, msg: Message):
    msg.ack()

  def reject(self, msg: Message, requeue=False):
    msg.reject(requeue=requeue)
    

