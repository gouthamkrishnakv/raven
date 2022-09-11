#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from msgpack import dumps
from pydantic import BaseModel
from raven.models.transfer_type import TransferType


class BaseResponse(BaseModel):
    """
    Base for all Response Bodies
    """

    ttype: TransferType

    def parse(self):
        return dumps(self.dict())
