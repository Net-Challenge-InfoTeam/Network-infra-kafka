import asyncio
import nats
from minio import Minio
from datetime import datetime

ACCESS_KEY = "node1"
SECRET_KEY = "12345678"
BUCKET_NAME = "stream"
DEST_FOLDER = "D:\\competition\\net challenge\\Network-infra-kafka\\test\\image"

async def main():
    print("NATS subscriber")
    nc = nats.NATS()
    await nc.connect("nats://10.32.187.188:4222")
    minio = Minio('10.32.187.188:9000', access_key=ACCESS_KEY, secret_key=SECRET_KEY, secure=False)
    f = open("result02.csv", "a")
    print("Connected to NATS server, and Minio server")
    
    async def message_handler(msg):
        subject = msg.subject
        reply = msg.reply
        data = msg.data.decode()
        if data == "test":
            print("start test")
            return
        print(f"Received a message on '{subject} {reply}': {data}")
        minio.fget_object(BUCKET_NAME, data, DEST_FOLDER + "/" + data)
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S.%f")
        f.write(f"{dt_string},{data}\n")
        f.flush()
        
        
    # Simple publisher and async subscriber via coroutine.
    try:
        while True:
            await nc.subscribe("foo", queue="worker", cb=message_handler)
    except KeyboardInterrupt:
        await nc.close()
        print("Finished.")
    except InterruptedError:
        print("Finished.")
        await nc.close()
    
if __name__ == '__main__':
    asyncio.run(main())