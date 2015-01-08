import os, signal, sys
import logging
import ./lib/crawl_request_handler

def main(): 
  LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
  logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
  logger = logging.getLogger(__name__)

  url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhhost:5672/%2f')
  handler = CrawlRequestHandler(url, logger) 

  def sigterm_handler(signal, frame):
    logger.info('Got SIGTERM, shutting down.')
    handler.stop()
  
  signal.signal(signal.SIGTERM, sigterm_handler)
  handler.run()

if __name__ == '__main__':
    main()
