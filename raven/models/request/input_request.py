from typing import Optional
from pydantic import Field

from .base import BaseRequest
from raven.models.transfer_type import TransferType


class InputRequestTest(BaseRequest):
    """
    # WARNING

    This is called `TEST` for a reason.

    **Do not use this for final design.**
    """
    ttype = Field(default=TransferType.INPUT_TEST)
    # TODO: Remove this, and make a more comprehensive request design
    #       input/
    #       | - input_start.py      (Or Request Begin?)
    #           # this could send platform and arch information, or other relevant info
    #           # start is followed by input_ack response, confirming server's intention
    #           # to start processing input information
    #       | - input_payload.py    (Or Input Body?)
    #       | - input_end.py        (Or Request Fin?)
    # Input Type (Evdev kind)
    itype: str = Field(default="NONAME")
    # Input Code (Evdev kind)
    icode: str | None = Field(default="NN_NONAME")
    # Field Value (Required sometimes)
    value: Optional[float] = Field(default=None)
