import os
from kafka import KafkaConsumer
from datetime import datetime

KAFKA_BOOTSTRAP_SERVERS = '10.32.103.147:9092'
KAFKA_TOPIC = 'pi1'
DEST_FOLDER = "D:\\competition\\net challenge\\Network-infra-kafka\\test\\image"

consumer = KafkaConsumer(KAFKA_TOPIC, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)

f = open("result01.csv", "a")
    
try:
    for message in consumer:
        image_data = message.value
        image_filename = message.key.decode('utf-8')
        producer_name = image_filename
        new_image_filename = f"image_{producer_name}_{message.key}.jpg"
        image_path = os.path.join(DEST_FOLDER, new_image_filename)
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