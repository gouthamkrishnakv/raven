#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# from asyncio import run, run_coroutine_threadsafe, to_thread
# from time import time

# from evdev.events import InputEvent
from evdev.device import InputDevice
from msgpack import dumps, loads
from raven.models.request.info_request import InfoRequest
from raven.models.request.input_request import InputRequestTest
from raven.models.response.info_response import InfoResponse
# from raven.models.response.ping_response import PingResponse
# from raven.models/dev/input/event4
from websockets.client import WebSocketClientProtocol, connect


async def run_loop(ws: WebSocketClientProtocol):
    pointer = InputDevice("/dev/input/event8")
    print(pointer.capabilities())
    for event in pointer.read_loop():
        await ws.send(
            InputRequestTest(
                itype=event.type, icode=event.code, value=event.value
            ).parse()
        )
        print(loads(await ws.recv()))


async def client():
    # timings = []
    async with connect("ws://localhost:8766") as websocket:
        # start = time()
        await websocket.send(dumps(InfoRequest().dict()))
        ans = await websocket.recv()
        ans_parsed = loads(ans)
        if "ttype" in ans_parsed:
            # if ans_parsed["ttype"] == TransferType.RPING:
            #     # PingResponse(**ans_parsed)
            #     ping_resp = PingResponse(**ans_parsed)
            #     print(ping_resp.dict())
            # if ans_parsed["ttype"] == TransferType.RINFO:
            #     # InfoResponse(**ans_parsed)
            # -- REMOVED FROM FOR LOOP
            info_resp = InfoResponse(**ans_parsed)
            print(info_resp.dict())
            pointer = InputDevice("/dev/input/event4")
            print(pointer.capabilities())
            for event in pointer.read_loop():
                await websocket.send(
                    InputRequestTest(
                        itype=event.type, icode=event.code, value=event.value
                    ).parse()
                )
                await websocket.close_connection()
        # end = time()
    #     timings.append(end - start)
    # print(f"The request-response took {sum(timings) / len(timings) * 1000 :.2f}ms")
