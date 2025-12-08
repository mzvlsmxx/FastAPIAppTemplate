import os

from confluent_kafka.admin import AdminClient
from confluent_kafka import Producer, Consumer, KafkaException


import logs as log


kafka_host = os.getenv('BROKER_HOST', '127.0.0.1')
kafka_port = int(os.getenv('BROKER_PORT', 7772))


class KafkaClient:
    """
    Kafka client wrapper class
    """
    
    @classmethod
    def check_access(cls) -> bool:
        """
        Checks connection to Kafka broker
        
        :return: bool indicating connection status
        """
        try:
            admin_client = AdminClient({'bootstrap.servers': f'{kafka_host}:{kafka_port}'})
            metadata = admin_client.list_topics(timeout=10)
            if metadata.brokers:
                return True
        
        except KafkaException as ex:
            log.errors.error(f'KafkaException occurred. ({ex})')
            return False
        
        except Exception as ex:
            log.errors.error(f'An Exception has occurred. ({ex})')
            return False

        return False
    
    @classmethod
    def get_bootstrap_servers_config(cls) -> dict[str, str]:
        """
        Get actual bootstrap.servers configuration info
        
        :return: Dict like {'bootstrap.servers': 'kafka_hostname:0000'}
        """
        return {'bootstrap.servers': f'{kafka_host}:{kafka_port}'}
        

        

# from confluent_kafka import Producer

# def delivery_report(err, msg):
#     """Callback function for message delivery acknowledgements."""
#     if err is not None:
#         print(f"Message delivery failed: {err}")
#     else:
#         print(f"Message delivered to topic {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")

# # Kafka broker configuration
# conf = {
#     'bootstrap.servers': 'localhost:9092',  # Replace with your Kafka broker address
#     'client.id': 'my-python-producer'
# }

# # Create a Producer instance
# producer = Producer(conf)

# topic = "my_test_topic"
# message_value = "Hello Kafka from Python!"
# message_key = "my_key"

# try:
#     # Produce the message
#     producer.produce(topic, key=message_key, value=message_value, callback=delivery_report)

#     # Wait for any outstanding messages to be delivered and delivery reports received
#     producer.flush()

# except Exception as e:
#     print(f"Error producing message: {e}")

# finally:
#     # Close the producer (optional, flush() handles most cases)
#     producer.poll(0) # Process any remaining callbacks