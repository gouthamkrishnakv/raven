#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Server Module

This everything required for the server module to work properly.
"""

from msgpack import dumps
from websockets.server import WebSocketServerProtocol

__all__ = ["dumps", "WebSocketServerProtocol"]
