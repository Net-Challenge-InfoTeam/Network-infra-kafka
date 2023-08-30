from kafka import KafkaConsumer
import os

# Kafka configuration
kafka_bootstrap_servers = 'your_kafka_broker_address:9092'  # Replace with your Kafka broker address
kafka_topic = 'camera_images'

# Create a Kafka consumer instance
consumer = KafkaConsumer(kafka_topic, bootstrap_servers=kafka_bootstrap_servers)

# Create a directory to save images
image_directory = 'received_images'
if not os.path.exists(image_directory):
    os.makedirs(image_directory)

try:
    for message in consumer:
        # Retrieve the image data from Kafka message
        image_data = message.value
        
        # Retrieve the original image filename from Kafka message's metadata
        image_filename = message.key.decode('utf-8')
        
        # Generate a unique filename based on the original filename and message offset
        image_filename_unique = f'{image_filename}_{message.offset:04d}.jpg'
        image_path = os.path.join(image_directory, image_filename_unique)
        
        # Save the image to the local file system
        with open(image_path, 'wb') as image_file:
            image_file.write(image_data)
        
        print(f"Image received and saved as '{image_path}'")
        
except KeyboardInterrupt:
    print("Consumer interrupted by user.")

finally:
    consumer.close()

