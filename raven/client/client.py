#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from time import time

from msgpack import dumps, loads
from raven.models.request.info_request import InfoRequest
from raven.models.response.info_response import InfoResponse
from raven.models.response.ping_response import PingResponse
from raven.models.transfer_type import TransferType
from websockets.client import connect


async def client():
    timings = []
    async with connect("ws://localhost:8766") as websocket:
        start = time()
        await websocket.send(dumps(InfoRequest().dict()))
        ans = await websocket.recv()
        ans_parsed = loads(ans)
        if "ttype" in ans_parsed:
            if ans_parsed["ttype"] == TransferType.RPING:
                # PingResponse(**ans_parsed)
                ping_resp = PingResponse(**ans_parsed)
                print(ping_resp.dict())
            if ans_parsed["ttype"] == TransferType.RINFO:
                # InfoResponse(**ans_parsed)
                info_resp = InfoResponse(**ans_parsed)
                print(info_resp.dict())
        end = time()
        timings.append(end - start)
    print(f"The request-response took {sum(timings) / len(timings) * 1000 :.2f}ms")
