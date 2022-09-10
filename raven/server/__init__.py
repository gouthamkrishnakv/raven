#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from raven.models.transfer_type import TransferType

from .info import info
from .ping import ping

fmatcher = {TransferType.PING: ping, TransferType.INFO: info}
