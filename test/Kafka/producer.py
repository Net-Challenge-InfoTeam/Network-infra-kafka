import cv2
from kafka import KafkaProducer
from datetime import datetime

KAFKA_BOOTSTRAP_SERVERS = '10.32.103.147:9092'
KAFKA_TOPIC = 'pi1'

producer = KafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

cap.set(cv2.CAP_PROP_FPS, 20)

frame_count = 0

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        filename = f'index-{frame_count}_timestamp-{c_time}.jpg'
        cv2.imwrite(filename, frame)
        
        with open(filename, 'rb') as image_file:
            image_data = image_file.read()

        c_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S:%f") # will send on paylaod in nats
        # Save the frame as a JPEG file
        producer.send(KAFKA_TOPIC, key=filename.encode('utf-8'), value=image_data)
        producer.flush()
        
        frame_count += 1
        if frame_count % 20 == 0: print(filename)
        
finally:
    producer.close()