from enum import IntEnum, IntFlag

class JackOptions(IntFlag):
    NULL = 0x00
    NO_START_SERVER = 0x01
    USE_EXACT_NAME = 0x02
    SERVER_NAME = 0x04
    LOAD_NAME = 0x08
    LOAD_INIT = 0x10
    SESSION_ID = 0x20
    
    OPEN_OPTIONS = SESSION_ID | SERVER_NAME | NO_START_SERVER | USE_EXACT_NAME
    LOAD_OPTIONS = LOAD_INIT | LOAD_NAME | USE_EXACT_NAME


class JackStatus(IntFlag):
    FAILURE = 0x01
    INVALID_OPTION = 0x02
    NAME_NOT_UNIQUE = 0x04
    SERVER_STARTED = 0x08
    SERVER_FAILED = 0x10
    SERVER_ERROR = 0x20
    NO_SUCH_CLIENT = 0x40
    LOAD_FAILURE = 0x80
    INIT_FAILURE = 0x100
    SHM_FAILURE = 0x200
    VERSION_ERROR = 0x400
    BACKEND_ERROR = 0x800
    CLIENT_ZOMBIE = 0x1000


class JackLatencyCallbackMode(IntEnum):
    CAPTURE = 0
    PLAYBACK = 1


class JackPortFlags(IntFlag):
    IS_INPUT = 0x01
    IS_OUTPUT = 0x02
    IS_PHYSICAL = 0x04
    CAN_MONITOR = 0x08
    IS_TERMINAL = 0x10
    IS_CONTROL_VOLTAGE = 0x100


class JackTransportState(IntEnum):
    STOPPED = 0
    ROLLING = 1
    LOOPING = 2
    STARTING = 3
    # JACK2 only:
    NET_STARTING = 4
    

class JackPositionBits(IntFlag):
    POSITION_BBT = 0x10
    POSITION_TIMECODE = 0x20
    BBT_FRAME_OFFSET = 0x40
    AUDIO_VIDEO_RATIO = 0x80
    VIDEO_FRAME_OFFSET = 0x100
    
    POSITION_MASK = (
        POSITION_BBT
        | POSITION_TIMECODE
        | BBT_FRAME_OFFSET
        | AUDIO_VIDEO_RATIO
        | VIDEO_FRAME_OFFSET)


class JackSessionEvenType(IntEnum):
    SAVE = 1
    SAVE_AND_QUIT = 2
    SAVE_TEMPLATE = 3


class JackSessionFlags(IntFlag):
    SAVE_ERROR = 0x01
    NEED_TERMINAL = 0x02


class JackPropertyChange(IntEnum):
    CREATED = 0
    CHANGED = 1
    DELETED = 2