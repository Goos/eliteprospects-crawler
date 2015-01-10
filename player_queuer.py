from src.amqp_client import AMQPClient, CrawlPlayerMessage

def main():
  client = AMQPClient()
  for id in range(2, 5):
    client.publish(CrawlPlayerMessage(id))
  
if __name__ == '__main__':
    main()
