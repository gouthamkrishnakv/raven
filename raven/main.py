#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from enum import Enum

from raven.server import ServerApp
from raven.client import ClientApp


class AppType(Enum):
    SERVER = "server"
    CLIENT = "client"


def main():
    # Create the argparse obj
    aparse = argparse.ArgumentParser(
        "raven",
        description="Raven Server/Client to share low-level data",
        epilog="Author: Goutham Krishna K V",
    )
    # Add type
    aparse.add_argument(
        "--type",
        default=AppType.CLIENT.value,
        choices=[AppType.SERVER.value, AppType.CLIENT.value],
    )
    args = aparse.parse_args()
    if args.type == AppType.CLIENT.value:
        print("Client Starting...")
        ClientApp.launch()
    else:
        print("Server Starting")
        ServerApp.launch()
