import os
from kafka import KafkaConsumer
from datetime import datetime

KAFKA_BOOTSTRAP_SERVERS = '10.32.103.147:9092'
KAFKA_TOPIC = 'pi1'

consumer = KafkaConsumer(KAFKA_TOPIC, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)

image_directory = 'received_images'
if not os.path.exists(image_directory):
    os.makedirs(image_directory)
    
try:
    for message in consumer:
        image_data = message.value
        image_filename = message.key.decode('utf-8')
        producer_name = image_filename
        new_image_filename = f"image_{producer_name}_{message.offset}.jpg"
        image_path = os.path.join(image_directory, new_image_filename)
        with open(image_path, 'wb') as image_file:
            image_file.write(image_data)
        print(f"Image received and saved as '{image_path}'")
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S.%f")
        f.write(f"{dt_string},{message.key}\n")
        f.flush()
    
except KeyboardInterrupt:
    print("Consumer interrupted by user.")
finally:
    consumer.close()