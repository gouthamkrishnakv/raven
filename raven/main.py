#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from asyncio import Event, Queue
import asyncio
import logging
from signal import SIGINT, sigwait
from threading import Thread
from evdev import InputDevice
from typing import Any, Protocol


class InputProtocol(Protocol):
    stop_ev: Event
    ipqueue: Queue

    def run_async(self):
        """
        Interface method for InputProtocol
        """
        ...

    async def report(self, val: Any):
        await self.ipqueue.put(val)


class PointerInput(InputProtocol):
    """
    Passing in pointer into here
    """

    dev: InputDevice
    delay: float

    def __init__(
        self, stop_ev: Event, ipqueue: Queue, dev: InputDevice, delay: float
    ) -> None:
        super().__init__()
        self.stop_ev = stop_ev
        self.ipqueue = ipqueue
        self.dev = dev
        self.delay = delay

    def run(self):
        pass

    async def run_async(self):
        self.dev.grab()
        while not self.stop_ev.is_set():
            if (input_ev := self.dev.read_one()) is not None:
                await self.report(input_ev)
            await asyncio.sleep(self.delay)
        self.dev.ungrab()


class AppThread(Thread):
    logger = logging.getLogger("AppThread")

    stop_ev: Event
    iqueue: Queue
    input_device: PointerInput

    delay: float = 1 / (120 * 8)

    def __init__(self, dev: str = "/dev/input/event8"):
        Thread.__init__(self)
        self.stop_ev = Event()
        self.iqueue = Queue()
        self.input_device = PointerInput(
            self.stop_ev, self.iqueue, InputDevice(dev), self.delay
        )

    def run(self):
        asyncio.run(self.mainloop())

    async def read_inp(self):
        self.logger.info("START")
        await self.input_device.run_async()
        self.logger.info("END")

    async def write_console(self):
        self.logger.info("START")
        while not self.stop_ev.is_set():
            if not self.iqueue.empty():
                self.logger.info(await self.iqueue.get())
            await asyncio.sleep(0.000_1)
        self.logger.info("STOPPING")
        while not self.iqueue.empty():
            self.logger.info(await self.iqueue.get())
        self.logger.info("END")

    async def mainloop(self):
        """
        Run Reading and Writing Tasks as asynchronous coroutines.
        """
        asyncio.create_task(self.read_inp())
        asyncio.create_task(self.write_console())
        while not self.stop_ev.is_set():
            await asyncio.sleep(0.1)
        asyncio.get_event_loop().stop()


def main():
    logging.basicConfig(level=logging.INFO)
    apt = AppThread()
    print("STARTING THREAD")
    apt.start()

    print("To stop app, click Ctrl+C")
    sigwait([SIGINT])

    apt.stop_ev.set()

    print("STOPPING THREAD")
    apt.join()
