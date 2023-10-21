import asyncio
import nats
from nats.errors import TimeoutError, NoServersError

async def main():
    nc = nats.NATS()
    
    await nc.connect("nats://10.32.187.188:4222")
    await nc.flush()

    try:
        while True:
            await nc.publish("foo", "test".encode())
            await nc.flush()
            await asyncio.sleep(1)
    except:
        return

if __name__ == '__main__':
    asyncio.run(main())
