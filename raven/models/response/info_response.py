from platform import machine
from platform import platform as pfm
from platform import release
from sys import byteorder

from pydantic import Field
from raven import __version__

from ..transfer_type import TransferType
from .base import BaseResponse


class InfoResponse(BaseResponse):
    ttype: TransferType = Field(default=TransferType.RINFO)
    arch: str = Field(default_factory=machine)
    platform: str = Field(default_factory=pfm)
    endianness: str = Field(default=byteorder)
    os_release: str = Field(default_factory=release)
    api_version: str = Field(default=__version__)
