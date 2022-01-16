"""
    Useful tools for parsing
"""
import io

from . import consts


def read_varint(data: io.FileIO) -> int:
    total = 0
    shift = 0
    while True:
        byte = data.read(1)
        if len(byte) == 0:
            raise EOFError
        # 01111111 mask to remove more data flag
        total |= (ord(byte) & 0x7F) << shift
        # Reached the end of the varint
        if not (ord(byte) & 0x80):
            return total & consts.VARINT_MASK

        shift += consts.VARINT_BLOCK_SIZE
        if shift >= consts.VARINT_MAX_SIZE:
            raise RuntimeError()
