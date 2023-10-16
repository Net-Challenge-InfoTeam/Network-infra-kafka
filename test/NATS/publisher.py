import asyncio
import nats
from nats.errors import TimeoutError, NoServersError

async def main():
    nc = nats.NATS()
    
    await nc.connect("nats://10.32.187.188:4222")

    for i in range(10):
        await nc.publish("foo", str(i).encode())

if __name__ == '__main__':
    asyncio.run(main())