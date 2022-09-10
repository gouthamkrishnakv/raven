#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Any, Dict, Optional
from .base import WebSocketServerProtocol, dumps
from raven.models.response.info_response import InfoResponse


async def info(ws: WebSocketServerProtocol, _: Optional[Dict[Any, Any]] = None):
    await ws.send(dumps(InfoResponse().dict()))
    await ws.close()
