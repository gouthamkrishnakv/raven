#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import logging
from evdev import InputDevice
from signal import SIGINT, sigwait
from threading import Event, Thread


class ClientApp(Thread):
    """
    Main Application Thread
    """

    logger = logging.getLogger("ClientApp")

    stop_ev: Event
    inqueue: asyncio.Queue
    dev: InputDevice

    delay = 1 / (60 * 2 * 5)

    def __init__(self, dev: str = "/dev/input/event8"):
        Thread.__init__(self)
        self.stop_ev = Event()
        self.inqueue = asyncio.Queue(maxsize=2000)
        self.dev = InputDevice(dev)

    def run(self):
        asyncio.run(self.apploop())

    async def apploop(self):
        # -- Add tasks here using asyncio.create_task
        # Stop if stop_ev is set
        asyncio.create_task(self.device_loop())
        while not self.stop_ev.is_set():
            await asyncio.sleep(0.1)

    async def device_loop(self):
        self.logger.info("STARTING")
        self.dev.grab()
        while not self.stop_ev.is_set():
            if (input_ev := self.dev.read_one()) is not None:
                await self.inqueue.put(input_ev)
            await asyncio.sleep(self.delay)
        self.dev.ungrab()
        self.logger.info("END")

    @staticmethod
    def launch():
        logging.basicConfig(level=logging.INFO)
        cla = ClientApp()
        ClientApp.logger.info("Starting Client")
        cla.start()
        # Wait till SIGINT
        ClientApp.logger.info("To stop app, click Ctrl+C")
        sigwait([SIGINT])

        # Set the stop event
        cla.stop_ev.set()

        # Wait to finish threads
        ClientApp.logger.info("Stopping Client")
