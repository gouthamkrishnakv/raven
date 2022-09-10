#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# -- Standard Libraries
import asyncio

# -- Package Imports
from msgpack import loads
from websockets.server import WebSocketServerProtocol, serve

# -- Self Imports
from ..models.response.base import BaseResponse

# The base "function-matcher" which runs async co-routine depending on the request type
# we're going to receive from the server.
from . import fmatcher


async def handle_conn(websocket: WebSocketServerProtocol):
    async for message in websocket:
        parsed_msg = loads(message)
        if "ttype" in parsed_msg:
            await fmatcher[BaseResponse(**parsed_msg).ttype](websocket, parsed_msg)


async def server():
    async with serve(handle_conn, "localhost", 8766):
        await asyncio.Future()
