#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from raven.models.transfer_type import TransferType
from pydantic import BaseModel


class BaseRequest(BaseModel):
    """
    Base for all Request Bodies
    """

    ttype: TransferType
