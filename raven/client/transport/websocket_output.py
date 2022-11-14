#!/usr/bin/env python3

from asyncio import Queue, sleep
from threading import Event

from websockets.client import connect


class WebsocketOutput:
    stop_event: Event
    url: str
    inqueue: Queue

    delay: float

    DEFAULT_DELAY = 1 / (60 * 2 * 5)

    def __init__(self, url: str, inqueue: Queue, delay: float = DEFAULT_DELAY):
        self.stop_event = Event()
        self.url = url
        self.inqueue = inqueue
        self.delay = delay

    async def start(self):
        """
        Start Output Thread
        """
        async with connect(self.url) as client:
            while not self.stop_event.is_set():
                if not self.inqueue.empty():
                    await client.send(str(await self.inqueue.get()))
                await sleep(self.delay)
            while not self.inqueue.empty():
                await client.send(str(await self.inqueue.get()))
            await client.close()
