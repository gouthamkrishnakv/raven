#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from queue import Queue
from threading import Lock, Thread

from time import sleep
from evdev import InputDevice, InputEvent
from signal import sigwait, SIGINT


class InputThread(Thread):
    tenable: bool = False
    lock: Lock = Lock()
    input_dev: InputDevice
    queue: Queue

    def __init__(self, input_device: str, shared_queue: Queue = Queue(maxsize=4096)):
        Thread.__init__(self)
        self.input_dev = InputDevice(input_device)
        self.queue = shared_queue

    def run(self):
        """
        Work on this later
        """
        # Grab the pointer
        self.input_dev.grab()
        print(">> POINTER GRABBED <<")
        while self.tenable:
            input_ev: InputEvent = self.input_dev.read_one()
            if input_ev is not None:
                # Event found
                # print(input_ev)
                self.queue.put(input_ev)
                print("EV")
            else:
                # Sleep for 2ms
                sleep(0.002)
        # Ungrab the pointer
        self.input_dev.ungrab()
        print("\n>> POINTER UNGRABBED <<")

    def enable(self):
        with self.lock:
            self.tenable = True

    def disable(self):
        with self.lock:
            self.tenable = False


class ConsoleOutput(Thread):
    queue: Queue
    tenable: bool

    def __init__(self, shared_queue: Queue, event_enable: bool):
        Thread.__init__(self)
        self.queue = shared_queue
        self.tenable = event_enable

    def run(self):
        # STOP when event == STOP OR queue is NOT EMPTY
        print(">> OUTPUT THREAD STARTED <<")
        while InputThread.tenable:
            # Print the queue value
            print("R")
            print(self.queue.get())
        print(">> OUTPUT THREAD STOPPED <<")


def main():
    it = InputThread("/dev/input/event4")
    ct = ConsoleOutput(it.queue, it.tenable)
    it.enable()
    # Start threads
    # - input thread
    it.start()
    # - output thread
    ct.start()
    # Wait until a SIGINT is thrown (Ctrl+C is hit)
    sigwait([SIGINT])
    # Send signal to stop the queue
    it.disable()
    # Stop the input thread
    it.join()
    # Stop the output thread
    ct.join()
    print("Thread Stopped")
