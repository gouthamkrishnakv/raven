#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pydantic import Field

from ..transfer_type import TransferType
from .base import BaseResponse


class PingResponse(BaseResponse):
    ttype: TransferType = Field(default=TransferType.RPING)
    message: str = Field(default="PONG")
