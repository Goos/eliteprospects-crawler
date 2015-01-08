import ./queue_handler

class CrawlRequestHandler(QueueHandler):
  EXCHANGE = 'crawl_requests'
  EXCHANGE_TYPE = 'topic'
  QUEUE = 'request_queue'
  ROUTING_KEY = 'crawl.players'

  def on_message(self, unused_channel, basic_deliver, properties, body):
    self._logger.info("crawlie")

