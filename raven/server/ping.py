#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Any, Dict, Optional
from raven.models.response.ping_response import PingResponse

from .base import WebSocketServerProtocol, dumps


async def ping(ws: WebSocketServerProtocol, _: Optional[Dict[Any, Any]] = None):
    """
    ping: `Ping Method`
    """
    # -- WARN: This print affects the performance
    # print("PING REQUESTED")
    await ws.send(dumps(PingResponse().dict()))
    await ws.close()
