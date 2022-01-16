import io
import struct
import time

import snappy

from . import consts, tools


class Replay:
    def __init__(self, data: io.FileIO) -> None:
        self.file = data

    def read_demo(self) -> bool:
        """Read a "DEMO" stye message, returns true if a message was read or false if not"""
        header = self.file.read(consts.HEADER_LEN)
        print(f"Header: {header}")
        if header != b"PBDEMS2\x00":
            return False

        offset = self.file.read(consts.OFFSET_LEN)
        print(f'Offset:{struct.unpack("I", offset)}')

        kind = tools.read_varint(self.file)
        # Check if message is compressed
        print(type(consts.DEMKind.DEM_IsCompressed))
        compressed = bool(kind & consts.DEMKind.DEM_IsCompressed)
        tick = tools.read_varint(self.file)
        size = tools.read_varint(self.file)

        message = self.file.read(size)
        # if compressed:
        #     message = snappy.uncompress(message)
        #     kind = kind & ~consts.DEMKind.DEM_IsCompressed
        print(
            f"Kind: {bin(kind)}\nTick: {tick}\nSize: {size}\nIsComp: {compressed}\nMessage: {message}\n"
        )
        return True

    def read_embed(self) -> bool:
        """Read an "embed" style message"""


def run():
    with open("data/6377407822_1190808105.dem", "rb") as ffile:
        replay = Replay(ffile)
        while replay.read_demo():
            time.sleep(0.5)


run()
