import time
import picamera
from kafka import KafkaProducer
from datetime import datetime

# Kafka configuration
kafka_bootstrap_servers = '10.32.103.147:9092'  # Replace with your Kafka broker address
kafka_topic = 'pi1' # 정한 토픽을 삽입

# Create a Kafka producer instance
producer = KafkaProducer(bootstrap_servers=kafka_bootstrap_servers)

# Initialize the PiCamera
camera = picamera.PiCamera()

try:
    while True:
        # Capture an image from the camera
        image_filename = 'image_pi1.jpg'  # You can customize the image filename set name role image_{pi name}
        camera.capture(image_filename)

        # Read the captured image
        with open(image_filename, 'rb') as image_file:
            image_data = image_file.read()

        # Send the image to Kafka topic
        key = 'pi1' # 파이별 해당하는 번호 부여
        producer.send(kafka_topic, key=key.encode('utf-8'), value=image_data)
        producer.flush()

        print(f"Image sent to Kafka topic '{kafka_topic}'")

        # Wait for 5 seconds before capturing the next image
        time.sleep(5)

finally:
    # Clean up resources
    camera.close()
    producer.close()