from kafka import KafkaConsumer
import os

# Kafka configuration
kafka_bootstrap_servers = '10.32.103.147:9092'  # Replace with your Kafka broker address
kafka_topic = 'pi1'

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
        
        # Split the filename to get the producer name and use it in the new filename
        producer_name = image_filename.split('_')[1]  # Assuming the format is "image_producerName.jpg"
        new_image_filename = f"image_{producer_name}_{message.offset}.jpg"
        
        # Generate a path to save the image in the image_directory
        image_path = os.path.join(image_directory, new_image_filename)
        
        # Save the image to the local file system
        with open(image_path, 'wb') as image_file:
            image_file.write(image_data)
        
        print(f"Image received and saved as '{image_path}'")
        
except KeyboardInterrupt:
    print("Consumer interrupted by user.")

finally:
    consumer.close()
