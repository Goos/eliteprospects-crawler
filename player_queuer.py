from src.amqp_client import AMQPClient, CrawlPlayerMessage

def main():
  client = AMQPClient()
  for id in range(1, 50001):
    client.publish(CrawlPlayerMessage(id))
  
if __name__ == '__main__':
    main()
