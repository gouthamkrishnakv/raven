#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pydantic import BaseModel
from raven.models.transfer_type import TransferType


class BaseResponse(BaseModel):
    ttype: TransferType
