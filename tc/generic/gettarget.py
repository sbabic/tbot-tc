import typing
import contextlib
import tbot
from tbot import tc
from tbot.machine import linux, board

@tbot.testcase
def getcpu(
    mach: typing.Optional[linux.LinuxMachine] = None,
) -> None:
    with contextlib.ExitStack() as cx:
        if mach is None:
            lh = cx.enter_context(tbot.acquire_lab())
            b = cx.enter_context(tbot.acquire_board(lh))
            lnx = cx.enter_context(tbot.acquire_linux(b))
        else:
            lnx = mach

        lnx.exec0("cat", "/proc/cpuinfo")

@tbot.testcase
def getlinuxversion(
    mach: typing.Optional[linux.LinuxMachine] = None,
) -> None:
    with contextlib.ExitStack() as cx:
        if mach is None:
            lh = cx.enter_context(tbot.acquire_lab())
            b = cx.enter_context(tbot.acquire_board(lh))
            lnx = cx.enter_context(tbot.acquire_linux(b))
        else:
            lnx = mach

        lnx.exec0("cat", "/proc/version")

@tbot.testcase
def getyoctoversion(
    mach: typing.Optional[linux.LinuxMachine] = None,
) -> None:
    with contextlib.ExitStack() as cx:
        if mach is None:
            lh = cx.enter_context(tbot.acquire_lab())
            b = cx.enter_context(tbot.acquire_board(lh))
            lnx = cx.enter_context(tbot.acquire_linux(b))
        else:
            lnx = mach

        lnx.exec0("cat", "/etc/os_release")

@tbot.testcase
def gettarget(
    mach: typing.Optional[linux.LinuxMachine] = None,
) -> None:
    with contextlib.ExitStack() as cx:
        if mach is None:
            lh = cx.enter_context(tbot.acquire_lab())
            b = cx.enter_context(tbot.acquire_board(lh))
            lnx = cx.enter_context(tbot.acquire_linux(b))
        else:
            lnx = mach

        tc.testsuite(
            getcpu,
            getlinuxversion,
            getyoctoversion,
            mach=lnx
        )
