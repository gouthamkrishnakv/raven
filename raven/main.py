#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from queue import Queue
from signal import SIGINT, sigwait
from threading import Event, Thread
from typing import Any
from evdev import InputEvent, InputDevice
import logging


logging.basicConfig(level=logging.DEBUG)


class InputThread(Thread):
    """
    Input Thread Class

    Takes in input, and puts it into a queue.
    """

    logger = logging.getLogger("InputThread")
    stop_ev: Event
    iqueue: Queue[InputEvent]
    input_device: InputDevice

    def __init__(self, input_device: str):
        Thread.__init__(self)
        self.stop_ev = Event()
        self.iqueue = Queue()
        self.input_device = InputDevice(input_device)

    def run(self):
        self.input_device.grab()
        self.logger.info("> POINTER GRABBED <")
        while not self.stop_ev.wait(0.000_01):
            input_ev: InputEvent = self.input_device.read_one()
            if input_ev is not None:
                # Event found
                # self.logger.debug("EV: %s", str(input_ev))
                self.iqueue.put(input_ev)
        self.input_device.ungrab()
        self.input_device.close()
        self.logger.info("> POINTER UNGRABBED <")


class ConsoleOutput(Thread):
    """
    Output Console Thread Class

    Accepts input, then prints back the output.
    """

    logger = logging.getLogger("ConsoleOutput")
    stop_ev: Event
    iqueue: Queue[Any]

    def __init__(self, queue: Queue[Any] = Queue()):
        Thread.__init__(self)
        self.stop_ev = Event()
        self.iqueue = queue

    def run(self):
        self.logger.info("CONSOLE OUTPUT STARTED")
        # Delay of 10 ms
        while not self.stop_ev.wait(0.01):
            if self.iqueue.qsize() > 0:
                self.logger.info("IREP: %s", str(self.iqueue.get()))
        self.logger.info("STOPPING CONSOLE THREAD")
        while not self.iqueue.empty():
            self.logger.info("IREP: %s", str(self.iqueue.get()))
        self.logger.info("CONSOLE THREAD STOPPED")


def main():
    """
    Main function
    """
    logger = logging.getLogger("main")
    # Create pointer input and console output threads
    logger.info("Creating input & output threads")
    it = InputThread("/dev/input/event4")
    ct = ConsoleOutput(it.iqueue)
    # Set the threads to run
    logger.info("Set the threads to run")
    # Start the threads
    logger.info("Start the threads")
    it.start()
    ct.start()
    # Wait for interrupt signal
    logger.info(">> To stop the application, click Ctrl+C")
    sigwait([SIGINT])
    # Stopping threads, first output, then input
    logger.info("Stopping threads")
    it.stop_ev.set()
    ct.stop_ev.set()
    # Waiting for the threads to stop
    logger.info("Waiting for threads to stop")
    it.join()
    ct.join(timeout=2)
    if ct.is_alive():
        logger.error("THREAD NOT STOPPED!!!")
    logger.info("EXITING")
