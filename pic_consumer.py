from kafka import KafkaConsumer
import os

# Kafka configuration
kafka_bootstrap_servers = '10.32.103.147:9092'  # Replace with your Kafka broker address
kafka_topic = 'pi_video'

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
        
        # Generate a unique image filename
        image_filename = os.path.join(image_directory, f'image_{message.offset}.jpg')
        
        # Save the image to the local file system
        with open(image_filename, 'wb') as image_file:
            image_file.write(image_data)
        
        print(f"Image received and saved as '{image_filename}'")
        
except KeyboardInterrupt:
    print("Consumer interrupted by user.")

finally:
    consumer.close()
