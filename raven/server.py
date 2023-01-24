#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from websockets.server import serve, WebSocketServerProtocol
from asyncio import run, Future


class ServerApp:
    def __init__(self) -> None:
        pass

    async def echo(self, protocol: WebSocketServerProtocol):
        """
        This prints the message.
        """
        async for message in protocol:
            print(message)

    async def main(self):
        async with serve(self.echo, "localhost", 8766):
            await Future()

    @staticmethod
    def launch():
        try:
            run(ServerApp().main())
        except KeyboardInterrupt:
            print("\rStopping")
