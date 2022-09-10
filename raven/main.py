#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# -- Standard Libraries
from argparse import ArgumentParser
from asyncio import run

# -- Package Imports
from raven.client.client import client
from raven.server.server import server


def run_client():
    try:
        run(client())
    except KeyboardInterrupt:
        print("Stopping Client")


# -- Run Server
def run_server():
    try:
        run(server())
    except KeyboardInterrupt:
        print("Stopping Server")


def main():
    parser: ArgumentParser = ArgumentParser(
        description="Raven CLI", epilog="Copyright (C) 2022 Goutham Krishna K V"
    )
    parser.add_argument("--type", choices=["server", "client"], default="client")
    args = parser.parse_args()

    if args.type == "client":
        run_client()
    elif args.type == "server":
        print("Trying to run server")
        run_server()
