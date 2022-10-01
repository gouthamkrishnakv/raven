#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from queue import Queue
from threading import Lock, Thread
from time import sleep
from typing import Any
import msgpack

from evdev import InputDevice, InputEvent


class InputReader(Thread):
    """
    Input Reader Class
    """

    lock: Lock
    queue: Queue[InputEvent]
    enable: bool
    device: InputDevice

    def __init__(self, dev: str = "/dev/input/event4") -> None:
        Thread.__init__(self)
        self.lock = Lock()
        self.queue = Queue()
        self.enable = True
        self.device = InputDevice(dev)
        self.capabilities = self.device.capabilities()

    def run(self):
        while self.enable:
            with self.lock:
                val = self.device.read_one()
                if val is not None:
                    self.queue.put(val)
                else:
                    # 0.01s delay
                    sleep(0.1)

    def itstop(self):
        with self.lock:
            self.enable = False


class ConsoleWriter(Thread):
    """
    Console Writer Class
    """

    lock: Lock
    enable: bool
    queue: Queue[Any]

    def __init__(self, c_queue: Queue[Any]) -> None:
        Thread.__init__(self)
        self.enable = True
        self.lock = Lock()
        self.queue = c_queue

    def run(self):
        # Read from queue until this disables
        # Add variable checks and assignments for cases where it could run in
        # non-single threaded situations
        enabled = False
        with self.lock:
            enabled = self.enable
        while enabled:
            with self.lock:
                print(self.queue.get())
                enabled = self.enable
        # After this is closed, clear out the queue
        while not self.queue.empty():
            print(self.queue.get())

    def ctstop(self):
        """
        Signal the thread to stop the server
        """
        with self.lock:
            self.enable = False


def main():
    it = InputReader()
    print(it.capabilities)
    print(msgpack.loads(msgpack.dumps(it.capabilities), strict_map_key=False))
    ct = ConsoleWriter(it.queue)
    try:
        it.start()
        ct.start()
    except KeyboardInterrupt:
        print(">>> STOPPING CONSOLE THREADS")
        it.itstop()
        it.join()
        ct.ctstop()
        ct.join()
