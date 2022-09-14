#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from threading import Lock


class ServerState:
    """
    This class holds the state of the server. This is a static variable.
    """

    _input_enabled: bool = False
    _lock = Lock()

    @staticmethod
    def get_input() -> bool:
        return ServerState._input_enabled

    @staticmethod
    def set_input(new_state: bool = False):
        with ServerState._lock:
            ServerState._input_enabled = new_state
