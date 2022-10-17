#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from asyncio import Event, Queue
import asyncio
import logging
from signal import SIGINT, sigwait
from threading import Thread
from evdev import InputDevice
from typing import Any, Protocol
from websockets.client import connect


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

    logger = logging.getLogger("PointerInput")

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
        self.logger.info("START")
        self.dev.grab()
        while not self.stop_ev.is_set():
            if (input_ev := self.dev.read_one()) is not None:
                await self.report(input_ev)
            await asyncio.sleep(self.delay)
        self.dev.ungrab()
        self.logger.info("END")


class OutputProtocol(Protocol):
    stop_ev: Event
    oqueue: Queue

    async def run_async(self):
        ...


class ConsoleOutput(OutputProtocol):
    """
    Pointer Input Class
    """

    logger = logging.getLogger("ConsoleOutput")

    def __init__(self, stop_ev: Event, oqueue: Queue):
        self.stop_ev = stop_ev
        self.oqueue = oqueue

    async def run_async(self):
        self.logger.info("START")
        while not self.stop_ev.is_set():
            if not self.oqueue.empty():
                self.logger.info(await self.oqueue.get())
            await asyncio.sleep(0.000_1)
        self.logger.info("STOPPING")
        while not self.oqueue.empty():
            self.logger.info(await self.oqueue.get())
        self.logger.info("END")


class WebsocketOutput(OutputProtocol):
    logger = logging.getLogger("WebSocketsOutput")
    # WebSockets URL
    uri: str

    def __init__(self, stop_ev: Event, oqueue: Queue, uri: str):
        self.stop_ev = stop_ev
        self.oqueue = oqueue
        self.uri = uri

    async def run_async(self):
        self.logger.info("START")
        async with connect(self.uri) as client:
            self.logger.info("CONNECTED")
            while not self.stop_ev.is_set():
                if not self.oqueue.empty():
                    await client.send(str(await self.oqueue.get()))
                await asyncio.sleep(0.001)
            self.logger.info("STOPPING")
            while not self.oqueue.empty():
                await client.send(str(await self.oqueue.get()))
            self.logger.info("CLOSING")
            await client.close()
        self.logger.info("END")


class AppThread(Thread):
    logger = logging.getLogger("AppThread")

    stop_ev: Event
    iqueue: Queue
    # We need multiple of these. The queue will be common and is shared
    input_protocol: InputProtocol
    output_protocol: OutputProtocol

    delay: float = 1 / (120 * 8)

    def __init__(self, dev: str = "/dev/input/event8"):
        Thread.__init__(self)
        self.stop_ev = Event()
        self.iqueue = Queue(maxsize=2000)
        self.input_protocol = PointerInput(
            self.stop_ev, self.iqueue, InputDevice(dev), self.delay
        )
        self.output_protocol = WebsocketOutput(
            self.stop_ev, self.iqueue, "ws://localhost:8766"
        )

    def run(self):
        asyncio.run(self.mainloop())

    async def read_inp(self):
        await self.input_protocol.run_async()

    async def write(self):
        await self.output_protocol.run_async()

    async def mainloop(self):
        """
        Run Reading and Writing Tasks as asynchronous coroutines.
        """
        # Add tasks to running event loop
        asyncio.create_task(self.read_inp())
        asyncio.create_task(self.write())
        # Wait till the event is stopped
        while not self.stop_ev.is_set():
            await asyncio.sleep(0.1)


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
