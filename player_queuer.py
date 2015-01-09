from lib.amqp_client import AMQPClient, CrawlPlayerMessage

def main():
  client = AMQPClient()
  client.publish(CrawlPlayerMessage(24047))
  
if __name__ == '__main__':
    main()
