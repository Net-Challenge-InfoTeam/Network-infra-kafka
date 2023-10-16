import asyncio
import nats
from nats.errors import TimeoutError, NoServersError

async def main():
    nc = nats.NATS()
    
    await nc.connect("nats://10.32.187.188:4222")
    
    async def message_handler(msg):
        subject = msg.subject
        reply = msg.reply
        data = msg.data.decode()
        print(f"Received a message on '{subject} {reply}': {data}")
    
    await nc.subscribe("foo", cb=message_handler)

    # Terminate connection to NATS.
    await nc.drain()

if __name__ == '__main__':
    while True:
        asyncio.run(main())