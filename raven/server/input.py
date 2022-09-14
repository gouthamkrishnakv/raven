#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Any, Dict, Optional

from raven.models.response.base import BaseResponse
from raven.models.transfer_type import TransferType

from .base import WebSocketServerProtocol, dumps


async def rinput(ws: WebSocketServerProtocol, msg: Optional[Dict[Any, Any]] = None):
    """
    input: `Input Method`
    """
    # -- WARN: This print affects performance
    print("INPUT REQUESTED")
    await ws.send(dumps(BaseResponse(ttype=TransferType.RPING).dict()))
