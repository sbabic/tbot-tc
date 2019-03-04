import contextlib
import typing
import time
import tbot
from tbot.machine import linux
import asyncio
import json
import os
import requests
import websockets
import sys

class SWUpdater:
    "" " Python helper class for SWUpdate " ""

    url_upload = 'http://{}:8080/upload'
    url_status = 'ws://{}:8080/ws'

    def __init__ (self, path_image, host_name):
        self.__image = path_image
        self.__host_name = host_name


    async def wait_update_finished(self, timeout = 300):
        tbot.log.message("Wait update finished")
        async def get_finish_messages ():
            async with websockets.connect(self.url_status.format(self.__host_name)) as websocket:
                while True:
                    message = await websocket.recv()
                    data = json.loads(message)

                    if data ["type"] != "message":
                        continue

                    tbot.log.message(data["text"])
                    if data ["text"] == "SWUPDATE successful !":
                        return 0

        await asyncio.wait_for(get_finish_messages(), timeout = timeout)

    def update (self, timeout = 300):
        tbot.log.message("Start uploading image...")
        try:
            response = requests.post(self.url_upload.format(self.__host_name), files = { 'file':open (self.__image, 'rb') })

            if response.status_code != 200:
                raise Exception ("Cannot upload software image: {}".  format (response.status_code))

            tbot.log.message("Software image uploaded successfully. Wait for installation to be finished...\n")
            asyncio.sleep(10)
            asyncio.get_event_loop().run_until_complete(self.wait_update_finished(timeout = timeout))

        except ValueError:
            print("No connection to host, exit")
            return 1

@tbot.testcase
def checkswupdate(
    mach: typing.Optional[linux.LinuxMachine] = None,
    **kwargs: typing.Any,
) -> None:
    with contextlib.ExitStack() as cx:
        if mach is None:
            lh = cx.enter_context(tbot.acquire_lab())
            b = cx.enter_context(tbot.acquire_board(lh))
            lnx = cx.enter_context(tbot.acquire_linux(b))
        else:
            lnx = mach

        version=lnx.exec("/usr/bin/swupdate", "--version")
        tbot.log.message(f"SWUpdate detected version {version}")

@tbot.testcase
def swupdateweb(
    mach: typing.Optional[linux.LinuxMachine] = None,
    ip = None,
    path = None,
) -> None:
    with contextlib.ExitStack() as cx:
        if mach is None:
            lh = cx.enter_context(tbot.acquire_lab())
            b = cx.enter_context(tbot.acquire_board(lh))
            lnx = cx.enter_context(tbot.acquire_linux(b))
        else:
            lnx = mach

        if ip is None:
            raise RuntimeError(f"IP Address is not set")
        if path is None:
            raise RuntimeError(f"Path to SWU is not set")

        return SWUpdater(path, ip).update ()
