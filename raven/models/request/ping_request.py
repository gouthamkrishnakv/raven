#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pydantic import Field

from .base import BaseRequest, TransferType


class PingRequest(BaseRequest):
    ttype: TransferType = Field(default=TransferType.PING)
    message: str = Field("PING")
