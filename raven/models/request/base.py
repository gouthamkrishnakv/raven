#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from raven.models.transfer_type import TransferType
from pydantic import BaseModel
from msgpack import dumps


class BaseRequest(BaseModel):
    """
    Base for all Request Bodies
    """

    ttype: TransferType

    def parse(self):
        return dumps(self.dict())
