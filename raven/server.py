#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from websockets.server import serve, WebSocketServerProtocol
from asyncio import run, Future


async def echo(protocol: WebSocketServerProtocol):
    async for message in protocol:
        await protocol.send(message)


async def main():
    async with serve(echo, "localhost", 8766):
        await Future()


run(main())
