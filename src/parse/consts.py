"""
    Replay parsing constants
"""

import enum


HEADER_LEN = 8
OFFSET_LEN = 4

VARINT_BLOCK_SIZE = 7
VARINT_MAX_SIZE = 5 * VARINT_BLOCK_SIZE  # Max size is 32 bits so use 35 due to block size
VARINT_MASK = (1 << 32) - 1  # extracts 32 LSBs from an oversized 35 bit varint


class DEMKind(enum.IntEnum):
    DEM_Stop = 0
    DEM_FileHeader = 1
    DEM_FileInfo = 2
    DEM_SyncTick = 3
    DEM_SendTables = 4
    DEM_ClassInfo = 5
    DEM_StringTables = 6
    DEM_Packet = 7
    DEM_SignonPacket = 8
    DEM_ConsoleCmd = 9
    DEM_CustomData = 10
    DEM_CustomDataCallbacks = 11
    DEM_UserCmd = 12
    DEM_FullPacket = 13
    DEM_SaveGame = 14
    DEM_IsCompressed = 112


class EmbedKind(enum.IntEnum):
    net_Tick = 4
    net_SetConVar = 6
    net_SignonState = 7
    svc_ServerInfo = 8
    svc_SendTable = 9
    svc_ClassInfo = 10
    svc_CreateStringTable = 12
    svc_UpdateStringTable = 13
    svc_VoiceInit = 14
    svc_VoiceData = 15
    svc_Sounds = 17
    svc_SetView = 18
    svc_UserMessage = 23
    svc_EntityMessage = 24
    svc_GameEvent = 25
    svc_PacketEntities = 26
    svc_TempEntities = 27
    svc_GameEventList = 30
