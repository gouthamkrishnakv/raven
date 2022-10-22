#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import logging
from queue import Queue
from signal import SIGINT, sigwait
from threading import Event, Thread


class ClientApp(Thread):
    """
    Main Application Thread
    """

    logger = logging.getLogger("ClientApp")

    stop_ev: Event
    inqueue: Queue

    def __init__(self, dev: str = "/dev/input/event4"):
        Thread.__init__(self)
        self.stop_ev = Event()
        self.inqueue = Queue(maxsize=2000)

    def run(self):
        asyncio.run(self.apploop())

    async def apploop(self):
        # -- Add tasks here using asyncio.create_task
        # Stop if stop_ev is set
        while not self.stop_ev.is_set():
            await asyncio.sleep(0.1)

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
