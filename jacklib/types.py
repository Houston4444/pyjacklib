from ctypes import (
    ARRAY,
    c_int,
    c_uint8,
    Structure,
    c_float,
    c_uint32,
    c_uint64,
    c_size_t,
    pointer,
    POINTER,
    c_int32,
    c_double,
    c_char_p,
    CFUNCTYPE,
    c_void_p
)


# Pre-Types
_c_enum = c_int
_c_uchar = c_uint8

class _jack_port(Structure):
    _fields_ = []


class _jack_client(Structure):
    _fields_ = []


# Types
jack_client_t = _jack_client
jack_default_audio_sample_t = c_float
jack_midi_data_t = _c_uchar
jack_nframes_t = c_uint32
jack_port_id_t = c_uint32
jack_port_t = _jack_port
jack_time_t = c_uint64
jack_unique_t = c_uint64
jack_uuid_t = c_uint64

jack_options_t = _c_enum  # JackOptions
jack_status_t = _c_enum  # JackStatus
jack_transport_state_t = _c_enum  # JackTransportState
jack_position_bits_t = _c_enum  # JackPositionBits
jack_session_event_type_t = _c_enum  # JackSessionEventType
jack_session_flags_t = _c_enum  # JackSessionFlags
jack_latency_callback_mode_t = _c_enum  # JackLatencyCallbackMode
jack_property_change_t = _c_enum  # JacKPropertyChange

# JACK2 only:
jack_port_type_id_t = c_uint32

# Structs
class jack_midi_event_t(Structure):
    time: jack_nframes_t
    size: c_size_t
    buffer: 'pointer[jack_midi_data_t]'
    _fields_ = [
        ("time", jack_nframes_t),
        ("size", c_size_t),
        ("buffer", POINTER(jack_midi_data_t))]


class jack_latency_range_t(Structure):
    min: jack_nframes_t
    max: jack_nframes_t
    _fields_ = [("min", jack_nframes_t), ("max", jack_nframes_t)]


class jack_position_t(Structure):
    unique_1: jack_unique_t
    usecs: jack_time_t
    frame_rate: jack_nframes_t
    frame: jack_nframes_t
    valid: jack_position_bits_t
    bar: c_int32
    beat: c_int32
    tick: c_int32
    bar_start_tick: c_double
    beats_per_bar: c_float
    beat_type: c_float
    ticks_per_beat: c_double
    beats_per_minute: c_double
    frame_time: c_double
    next_time: c_double
    bbt_offset: jack_nframes_t
    audio_frames_per_video_frame: c_float
    video_offset: jack_nframes_t
    padding: ARRAY(c_int32, 7)
    unique_2: jack_unique_t
    _fields_ = [
        ("unique_1", jack_unique_t),
        ("usecs", jack_time_t),
        ("frame_rate", jack_nframes_t),
        ("frame", jack_nframes_t),
        ("valid", jack_position_bits_t),
        ("bar", c_int32),
        ("beat", c_int32),
        ("tick", c_int32),
        ("bar_start_tick", c_double),
        ("beats_per_bar", c_float),
        ("beat_type", c_float),
        ("ticks_per_beat", c_double),
        ("beats_per_minute", c_double),
        ("frame_time", c_double),
        ("next_time", c_double),
        ("bbt_offset", jack_nframes_t),
        ("audio_frames_per_video_frame", c_float),
        ("video_offset", jack_nframes_t),
        ("padding", ARRAY(c_int32, 7)),
        ("unique_2", jack_unique_t),
    ]


class jack_session_event_t(Structure):
    _fields_ = [
        ("type", jack_session_event_type_t),
        ("session_dir", c_char_p),
        ("client_uuid", c_char_p),
        ("command_line", c_char_p),
        ("flags", jack_session_flags_t),
        ("future", c_uint32),
    ]


class jack_session_command_t(Structure):
    _fields_ = [
        ("uuid", c_char_p),
        ("client_name", c_char_p),
        ("command", c_char_p),
        ("flags", jack_session_flags_t),
    ]


class jack_property_t(Structure):
    key: c_char_p
    data: c_char_p
    type: c_char_p
    _fields_ = [("key", c_char_p), ("data", c_char_p), ("type", c_char_p)]


class jack_description_t(Structure):
    subject: jack_uuid_t
    property_cnt: c_uint32
    properties: 'pointer[jack_property_t]'
    property_size: c_uint32
    _fields_ = [
        ("subject", jack_uuid_t),
        ("property_cnt", c_uint32),
        ("properties", POINTER(jack_property_t)),
        ("property_size", c_uint32),
    ]


# Callbacks
JackThreadCallback = CFUNCTYPE(c_void_p, c_void_p)
JackTimebaseCallback = CFUNCTYPE(
    None,
    jack_transport_state_t,
    jack_nframes_t,
    POINTER(jack_position_t),
    c_int,
    c_void_p
)
JackPropertyChangeCallback = CFUNCTYPE(
    None, jack_uuid_t, c_char_p, jack_property_change_t, c_void_p
)
JackErrorCallback = CFUNCTYPE(None, c_char_p)