#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pydantic import Field

from raven.models.transfer_type import TransferType
from .base import BaseRequest


class InfoRequest(BaseRequest):
    ttype = Field(default=TransferType.INFO)
