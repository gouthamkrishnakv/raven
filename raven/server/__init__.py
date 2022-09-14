#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from asyncio import Future
from websockets.server import WebSocketServerProtocol, serve
from msgpack import loads

from raven.models.transfer_type import TransferType
from raven.models.response import BaseResponse

from .info import info
from .ping import ping

fmatcher = {TransferType.PING: ping, TransferType.INFO: info}


async def handle_conn(websocket: WebSocketServerProtocol):
    async for message in websocket:
        parsed_msg = loads(message)
        if "ttype" in parsed_msg:
            await fmatcher[BaseResponse(**parsed_msg).ttype](websocket, parsed_msg)


async def server():
    async with serve(handle_conn, "localhost", 8766):
        await Future()
