"""
Input Device Module
"""

import asyncio
import logging
from threading import Event
from evdev import InputDevice


class DeviceInput:
    logger = logging.getLogger("DeviceInput")

    dev: InputDevice
    inqueue: asyncio.Queue
    stop_ev: Event
    delay: float

    DEFAULT_DELAY = 1 / (60 * 2 * 5)

    def __init__(
        self,
        dev: InputDevice,
        inqueue: asyncio.Queue,
        stop_ev: Event,
        delay: float = DEFAULT_DELAY,
    ):
        self.dev = dev
        self.inqueue = inqueue
        self.stop_ev = stop_ev
        self.delay = delay

    async def start(self):
        self.logger.info("STARTING")
        caps = self.dev.capabilities(verbose=False)
        for key in caps:
            print("KEY: {}".format(key))
            tup = caps[key]
            print(f"CODE: {tup[0]}")
            print(f"VAL: {tup[1:]}")
        self.dev.grab()
        while not self.stop_ev.is_set():
            if (input_ev := self.dev.read_one()) is not None:
                await self.inqueue.put(input_ev)
            await asyncio.sleep(self.delay)
        self.dev.ungrab()
        self.logger.info("END")
