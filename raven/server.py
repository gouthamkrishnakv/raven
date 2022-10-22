#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from websockets.server import serve, WebSocketServerProtocol
from asyncio import run, Future


async def echo(protocol: WebSocketServerProtocol):
    """
    This prints the message.
    """
    async for message in protocol:
        print(message)


async def main():
    async with serve(echo, "localhost", 8766):
        await Future()


def server():
    try:
        run(main())
    except KeyboardInterrupt:
        print("\rStopping")
