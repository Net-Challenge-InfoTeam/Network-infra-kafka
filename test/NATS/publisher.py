import asyncio
import nats
from nats.errors import TimeoutError, NoServersError
import cv2
from minio import Minio
import time
from datetime import datetime

ACCESS_KEY = "producer"
SECRET_KEY = "bqXn02k2BJj8bEvXrtHPMWGBcTRosZCAGzxP7YuP"
BUCKET_NAME = 'stream'

async def main():
    nc = nats.NATS()
    
    print("Connecting to NATS...")
    await nc.connect("nats://10.32.187.188:4222")
    await nc.publish("foo", "test".encode())
    await nc.flush()
    print("Completed")
 
    MINIO_CLIENT = Minio('10.32.187.188:9000', access_key=ACCESS_KEY, secret_key=SECRET_KEY, secure=False)
    # Check if bucket exists, else create
    if not MINIO_CLIENT.bucket_exists(BUCKET_NAME):
        MINIO_CLIENT.make_bucket(BUCKET_NAME)
    print("setting...")
    # Capture video from the default camera
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    # Set capture frame rate
    cap.set(cv2.CAP_PROP_FPS, 20)
    print("ready")
    frame_count = 0
    temp = 0
    try:
        print("start")
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            c_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S:%f") # will send on paylaod in nats
            # Save the frame as a JPEG file
            filename = f'index-{frame_count}_timestamp-{c_time}.jpg'
            cv2.imwrite(filename, frame)

            # Upload the frame to MinIO
            MINIO_CLIENT.fput_object(BUCKET_NAME, filename, filename)
            await nc.publish("foo", filename.encode())
            await nc.flush()
            frame_count += 1
            temp += 1
            if temp == 20: temp = 0; print(filename)

    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    asyncio.run(main())