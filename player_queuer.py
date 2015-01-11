from src.amqp_client import AMQPClient, CrawlPlayerMessage

def main():
  client = AMQPClient()

  for id in range(221185, 336213):
    client.publish(CrawlPlayerMessage(id))
  
if __name__ == '__main__':
    main()
