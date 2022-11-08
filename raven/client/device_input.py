from evdev import InputDevice
from threading import Thread
import asyncio
import logging
from asyncio import Event


class DeviceInput(Thread):
    """
    Device Input

    This thread reads from projects, and
    """

    # Logging
    logger = logging.getLogger("DeviceInput")

    # Thread-scoped variables
    dev: InputDevice
    stop_ev: Event
    ipqueue: asyncio.Queue
    delay: float

    def __init__(self, dev: InputDevice, ipqueue: asyncio.Queue, delay: float):
        Thread.__init__(self)
        self.stop_ev = Event()
        self.dev = dev
        self.ipqueue = ipqueue
        self.delay = delay

    def run(self):
        asyncio.run(self.async_loop())

    async def async_loop(self):
        self.logger.info("STARTING")
        self.dev.grab()
        while not self.stop_ev.is_set():
            if (input_ev := self.dev.read_one()) is not None:
                await self.ipqueue.put(input_ev)
            await asyncio.sleep(self.delay)
        self.dev.ungrab()
        self.logger.info("END")
