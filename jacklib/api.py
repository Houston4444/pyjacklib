"""JACK ctypes definitions for usage in python applications."""

# Copyright (C) 2010-2020 Filipe Coelho <falktx@falktx.com>
#               2016-2022 Christopher Arndt <info@chrisarndt.de>
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# For a full copy of the GNU General Public License see the file COPYING.md.

# -------------------------------------------------------------------------------------------------
# Imports (Global)

import sys
from collections import namedtuple
from ctypes import (
    ARRAY,
    CFUNCTYPE,
    POINTER,
    Structure,
    byref,
    c_char_p,
    c_double,
    c_float,
    c_int,
    c_int32,
    c_size_t,
    c_uint8,
    c_uint32,
    c_uint64,
    c_ulong,
    c_void_p,
    cdll,
    pointer,
    sizeof,
)
from typing import Callable, Iterator

# import locals
from enums import (
    JackOptions,
    JackStatus,
    JackLatencyCallbackMode,
    JackPortFlags,
    JackTransportState,
    JackPositionBits,
    JackSessionEvenType,
    JackSessionFlags,
    JackPropertyChange
)

# -------------------------------------------------------------------------------------------------
# Load JACK shared library


def _is_python_64bit():
    return sizeof(c_void_p) == 8


try:
    if sys.platform == "darwin":
        _libname = "libjack.dylib"
    elif sys.platform in ("win32", "cygwin"):
        if _is_python_64bit():
            _libname = "libjack64.dll"
        else:
            _libname = "libjack.dll"
    else:
        _libname = "libjack.so.0"

    jlib = cdll.LoadLibrary(_libname)
except OSError:
    raise ImportError("JACK is not available in this system")


# -------------------------------------------------------------------------------------------------
# JACK2 test

try:
    if jlib.jack_get_version_string:
        JACK2 = True
    else:
        JACK2 = False
except AttributeError:
    JACK2 = False


# -------------------------------------------------------------------------------------------------
# Pre-Types

c_enum = c_int
c_uchar = c_uint8


class _jack_port(Structure):
    _fields_ = []


class _jack_client(Structure):
    _fields_ = []


# -------------------------------------------------------------------------------------------------
# Defines

ENCODING = "utf-8"
JACK_MAX_FRAMES = 4294967295
JACK_LOAD_INIT_LIMIT = 1024
JACK_DEFAULT_AUDIO_TYPE = "32 bit float mono audio"
JACK_DEFAULT_MIDI_TYPE = "8 bit raw midi"

JACK_UUID_SIZE = 36
JACK_UUID_STRING_SIZE = JACK_UUID_SIZE + 1
JACK_UUID_EMPTY_INITIALIZER = 0

# Meta data
_JACK_METADATA_PREFIX = "http://jackaudio.org/metadata/"
JACK_METADATA_CONNECTED = _JACK_METADATA_PREFIX + "connected"
JACK_METADATA_EVENT_TYPES = _JACK_METADATA_PREFIX + "event-types"
JACK_METADATA_HARDWARE = _JACK_METADATA_PREFIX + "hardware"
JACK_METADATA_ICON_LARGE = _JACK_METADATA_PREFIX + "icon-large"
JACK_METADATA_ICON_NAME = _JACK_METADATA_PREFIX + "icon-name"
JACK_METADATA_ICON_SMALL = _JACK_METADATA_PREFIX + "icon-small"
JACK_METADATA_ORDER = _JACK_METADATA_PREFIX + "order"
JACK_METADATA_PORT_GROUP = _JACK_METADATA_PREFIX + "port-group"
JACK_METADATA_PRETTY_NAME = _JACK_METADATA_PREFIX + "pretty-name"
JACK_METADATA_SIGNAL_TYPE = _JACK_METADATA_PREFIX + "signal-type"


# -------------------------------------------------------------------------------------------------
# Helper functions


def _e(s, encoding=ENCODING):
    if encoding:
        return s.encode(encoding)
    return s


def _d(s, encoding=ENCODING):
    if encoding:
        return s.decode(encoding)
    return s


# -------------------------------------------------------------------------------------------------
# Types

jack_client_t = _jack_client
jack_default_audio_sample_t = c_float
jack_midi_data_t = c_uchar
jack_nframes_t = c_uint32
jack_port_id_t = c_uint32
jack_port_t = _jack_port
jack_time_t = c_uint64
jack_unique_t = c_uint64
jack_uuid_t = c_uint64

jack_options_t = c_enum  # JackOptions
jack_status_t = c_enum  # JackStatus
jack_transport_state_t = c_enum  # JackTransportState
jack_position_bits_t = c_enum  # JackPositionBits
jack_session_event_type_t = c_enum  # JackSessionEventType
jack_session_flags_t = c_enum  # JackSessionFlags
jack_latency_callback_mode_t = c_enum  # JackLatencyCallbackMode
jack_property_change_t = c_enum  # JacKPropertyChange

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


# -------------------------------------------------------------------------------------------------
# Callbacks

JackThreadCallback = CFUNCTYPE(c_void_p, c_void_p)
JackTimebaseCallback = CFUNCTYPE(
    None, jack_transport_state_t, jack_nframes_t, POINTER(jack_position_t), c_int, c_void_p
)
JackErrorCallback = CFUNCTYPE(None, c_char_p)


# -------------------------------------------------------------------------------------------------
# Functions

try:
    jlib.jack_get_version_string.argtypes = None
    jlib.jack_get_version_string.restype = c_char_p
except AttributeError:
    jlib.jack_get_version_string = None

try:
    jlib.jack_client_open.argtypes = [c_char_p, jack_options_t, POINTER(jack_status_t), c_char_p]
    jlib.jack_client_open.restype = POINTER(jack_client_t)
except AttributeError:
    jlib.jack_client_open = None

try:
    jlib.jack_client_rename.argtypes = [POINTER(jack_client_t), c_char_p]
    jlib.jack_client_rename.restype = c_char_p
except AttributeError:
    jlib.jack_client_rename = None

try:
    jlib.jack_client_close.argtypes = [POINTER(jack_client_t)]
    jlib.jack_client_close.restype = c_int
except AttributeError:
    jlib.jack_client_close = None

try:
    jlib.jack_client_name_size.argtypes = None
    jlib.jack_client_name_size.restype = c_int
except AttributeError:
    jlib.jack_client_name_size = None

try:
    jlib.jack_get_client_name.argtypes = [POINTER(jack_client_t)]
    jlib.jack_get_client_name.restype = c_char_p
except AttributeError:
    jlib.jack_get_client_name = None

try:
    jlib.jack_activate.argtypes = [POINTER(jack_client_t)]
    jlib.jack_activate.restype = c_int
except AttributeError:
    jlib.jack_activate = None

try:
    jlib.jack_deactivate.argtypes = [POINTER(jack_client_t)]
    jlib.jack_deactivate.restype = c_int
except AttributeError:
    jlib.jack_deactivate = None

try:
    jlib.jack_get_client_pid.argtypes = [c_char_p]
    jlib.jack_get_client_pid.restype = c_int
except AttributeError:
    jlib.jack_get_client_pid = None

try:
    jlib.jack_is_realtime.argtypes = [POINTER(jack_client_t)]
    jlib.jack_is_realtime.restype = c_int
except AttributeError:
    jlib.jack_is_realtime = None


# JACK2 only:
def get_version_string() -> str:
    if jlib.jack_get_version_string:
        return _d(jlib.jack_get_version_string())

    return ''


def client_open(client_name: str, options, status, uuid="") -> 'pointer[jack_client_t]':
    if jlib.jack_client_open:
        return jlib.jack_client_open(
            _e(client_name), options, status, _e(uuid) if uuid else None)

    return None


def client_rename(client, new_name: str):
    if jlib.jack_client_rename:
        return jlib.jack_client_rename(client, _e(new_name))

    return None


def client_close(client) -> int:
    if jlib.jack_client_close:
        return jlib.jack_client_close(client)

    return -1


def client_name_size() -> int:
    if jlib.jack_client_name_size:
        return jlib.jack_client_name_size()

    return 0


def get_client_name(client):
    if jlib.jack_get_client_name:
        return jlib.jack_get_client_name(client)

    return None


def activate(client) -> int:
    if jlib.jack_activate:
        return jlib.jack_activate(client)

    return -1


def deactivate(client) -> int:
    if jlib.jack_deactivate:
        return jlib.jack_deactivate(client)

    return -1


# JACK2 only:
def get_client_pid(name: str) -> int:
    if jlib.jack_get_client_pid:
        return jlib.jack_get_client_pid(_e(name))

    return 0


def is_realtime(client) -> int:
    if jlib.jack_is_realtime:
        return jlib.jack_is_realtime(client)

    return 0


# -------------------------------------------------------------------------------------------------
# Non-Callback API

_thread_callback = None

try:
    jlib.jack_cycle_wait.argtypes = [POINTER(jack_client_t)]
    jlib.jack_cycle_wait.restype = jack_nframes_t
except AttributeError:
    jlib.jack_cycle_wait = None

try:
    jlib.jack_cycle_signal.argtypes = [POINTER(jack_client_t), c_int]
    jlib.jack_cycle_signal.restype = None
except AttributeError:
    jlib.jack_cycle_signal = None

try:
    jlib.jack_set_process_thread.argtypes = [POINTER(jack_client_t), JackThreadCallback, c_void_p]
    jlib.jack_set_process_thread.restype = c_int
except AttributeError:
    jlib.jack_set_process_thread = None


def cycle_wait(client):
    if jlib.jack_cycle_wait:
        return jlib.jack_cycle_wait(client)

    return 0


def cycle_signal(client, status):
    if jlib.jack_cycle_signal:
        jlib.jack_cycle_signal(client, status)


def set_process_thread(client, thread_callback, arg):
    if jlib.jack_set_process_thread:
        global _thread_callback
        _thread_callback = JackThreadCallback(thread_callback)
        return jlib.jack_set_process_thread(client, _thread_callback, arg)

    return -1


# -------------------------------------------------------------------------------------------------
# Client Callbacks

# this list is used to prevent added elements to be removed by python cleaner
_used_callbacks = list[CFUNCTYPE]()

JackTimebaseCallback = CFUNCTYPE(
    None, jack_transport_state_t, jack_nframes_t, POINTER(jack_position_t), c_int, c_void_p
)
JackPropertyChangeCallback = CFUNCTYPE(
    None, jack_uuid_t, c_char_p, jack_property_change_t, c_void_p
)
JackErrorCallback = CFUNCTYPE(None, c_char_p)


class _Cb:
    def __init__(self, ref: str, callback: CFUNCTYPE, restype, suffix='_callback'):
        self.ref = ref
        self.callback = callback
        self.restype = restype
        self.setter_name = ref + suffix
        try:
            func = getattr(globals()['jlib'], 'jack_' + self.setter_name)
            func.argstypes = [POINTER(jack_client_t), self.callback, c_void_p]
            func.restype = self.restype
            self.jlib_func = func
        except AttributeError:
            self.jlib_func = None


_CBS = (
    _Cb('set_thread_init',
        CFUNCTYPE(None, c_void_p),
        c_int),
    _Cb('on_shutdown',
        CFUNCTYPE(None, c_void_p),
        None,
        suffix=''),
    _Cb('on_info_shutdown',
        CFUNCTYPE(None, jack_status_t, c_char_p, c_void_p),
        None,
        suffix=''),
    _Cb('set_process',
        CFUNCTYPE(c_int, jack_nframes_t, c_void_p),
        c_int),
    _Cb('set_freewheel',
        CFUNCTYPE(None, c_int, c_void_p),
        c_int),
    _Cb('set_buffer_size',
        CFUNCTYPE(c_int, jack_nframes_t, c_void_p),
        c_int),
    _Cb('set_sample_rate',
        CFUNCTYPE(c_int, jack_nframes_t, c_void_p),
        c_int),
    _Cb('set_client_registration',
        CFUNCTYPE(None, c_char_p, c_int, c_void_p),
        c_int),
    _Cb('set_client_rename',
        CFUNCTYPE(c_int, c_char_p, c_char_p, c_void_p),
        c_int),
    _Cb('set_port_registration',
        CFUNCTYPE(None, jack_port_id_t, c_int, c_void_p),
        c_int),
    _Cb('set_port_connect',
        CFUNCTYPE(None, jack_port_id_t, jack_port_id_t, c_int, c_void_p),
        c_int),
    _Cb('set_port_rename',
        CFUNCTYPE(None, jack_port_id_t, c_char_p, c_char_p, c_void_p),
        c_int),
    _Cb('set_graph_order',
        CFUNCTYPE(c_int, c_void_p),
        c_int),
    _Cb('set_xrun',
        CFUNCTYPE(c_int, c_void_p),
        c_int),
    _Cb('set_latency',
        CFUNCTYPE(None, jack_latency_callback_mode_t, c_void_p),
        c_int),
    # other callbacks
    _Cb('set_sync',
        CFUNCTYPE(c_int, jack_transport_state_t, POINTER(jack_position_t), c_void_p),
        c_int),
    _Cb('set_session',
        CFUNCTYPE(None, POINTER(jack_session_event_t), c_void_p),
        c_int),
    _Cb('set_property_change',
        CFUNCTYPE(None, jack_uuid_t, c_char_p, jack_property_change_t, c_void_p),
        c_int),
    ## following is not really a callback setter, but it uses the same scheme
    # _Cb('set_process_thread',
    #     CFUNCTYPE(c_void_p, c_void_p),
    #     c_int,
    #     suffix='')
    )


def callback_setter(func: Callable):
    ''' decorator for callback setter.
        note that the decorated function is never executed
        everything depends on its name. '''
    for _cb in _CBS:
        if func.__name__ == _cb.setter_name:
            break
    else:
        raise BaseException(
            f'callback_setter decorator: no _Cb found with setter_name "{func.__name__}"')
    
    def wrapper(client, callback, arg):
        if _cb.jlib_func is None:
            if _cb.restype is c_int:
                return -1
            return None
        
        _callback = _cb.callback(callback)
        _used_callbacks.append(_callback)
        return _cb.jlib_func(client, _callback, arg)
    return wrapper

@callback_setter
def set_thread_init_callback(client, thread_init_callback, arg) -> int:
    ...

@callback_setter
def on_shutdown(client, shutdown_callback, arg):
    ...

@callback_setter
def on_info_shutdown(client, info_shutdown_callback, arg):
    ...

@callback_setter
def set_process_callback(client, process_callback, arg) -> int:
    ...

@callback_setter
def set_freewheel_callback(client, freewheel_callback, arg) -> int:
    ...

@callback_setter
def set_buffer_size_callback(client, bufsize_callback, arg) -> int:
    ...

@callback_setter
def set_sample_rate_callback(client, srate_callback, arg) -> int:
    ...

@callback_setter
def set_client_registration_callback(client, client_registration_callback, arg) -> int:
    ...

# JACK2 only:
@callback_setter
def set_client_rename_callback(client, client_rename_callback, arg) -> int:
    ...

@callback_setter
def set_port_registration_callback(client, port_registration_callback, arg) -> int:
    ...

@callback_setter
def set_port_connect_callback(client, connect_callback, arg) -> int:
    ...

# JACK2 only:
@callback_setter
def set_port_rename_callback(client, rename_callback, arg) -> int:
    ...

@callback_setter
def set_graph_order_callback(client, graph_callback, arg) -> int:
    ...

@callback_setter
def set_xrun_callback(client, xrun_callback, arg) -> int:
    ...

@callback_setter
def set_latency_callback(client, latency_callback, arg) -> int:
    ...

# -------------------------------------------------------------------------------------------------
# Server Control

jlib.jack_set_freewheel.argtypes = [POINTER(jack_client_t), c_int]
jlib.jack_set_freewheel.restype = c_int

jlib.jack_set_buffer_size.argtypes = [POINTER(jack_client_t), jack_nframes_t]
jlib.jack_set_buffer_size.restype = c_int

jlib.jack_get_sample_rate.argtypes = [POINTER(jack_client_t)]
jlib.jack_get_sample_rate.restype = jack_nframes_t

jlib.jack_get_buffer_size.argtypes = [POINTER(jack_client_t)]
jlib.jack_get_buffer_size.restype = jack_nframes_t

jlib.jack_engine_takeover_timebase.argtypes = [POINTER(jack_client_t)]
jlib.jack_engine_takeover_timebase.restype = c_int

jlib.jack_cpu_load.argtypes = [POINTER(jack_client_t)]
jlib.jack_cpu_load.restype = c_float


def set_freewheel(client, onoff):
    return jlib.jack_set_freewheel(client, onoff)


def set_buffer_size(client, nframes):
    return jlib.jack_set_buffer_size(client, nframes)


def get_sample_rate(client):
    return jlib.jack_get_sample_rate(client)


def get_buffer_size(client):
    return jlib.jack_get_buffer_size(client)


def engine_takeover_timebase(client):
    return jlib.jack_engine_takeover_timebase(client)


def cpu_load(client):
    return jlib.jack_cpu_load(client)


# -------------------------------------------------------------------------------------------------
# Port Functions

jlib.jack_port_register.argtypes = [POINTER(jack_client_t), c_char_p, c_char_p, c_ulong, c_ulong]
jlib.jack_port_register.restype = POINTER(jack_port_t)

jlib.jack_port_unregister.argtypes = [POINTER(jack_client_t), POINTER(jack_port_t)]
jlib.jack_port_unregister.restype = c_int

jlib.jack_port_get_buffer.argtypes = [POINTER(jack_port_t), jack_nframes_t]
jlib.jack_port_get_buffer.restype = c_void_p

jlib.jack_port_name.argtypes = [POINTER(jack_port_t)]
jlib.jack_port_name.restype = c_char_p

jlib.jack_port_short_name.argtypes = [POINTER(jack_port_t)]
jlib.jack_port_short_name.restype = c_char_p

jlib.jack_port_flags.argtypes = [POINTER(jack_port_t)]
jlib.jack_port_flags.restype = c_int

jlib.jack_port_type.argtypes = [POINTER(jack_port_t)]
jlib.jack_port_type.restype = c_char_p

if JACK2:
    jlib.jack_port_type_id.argtypes = [POINTER(jack_port_t)]
    jlib.jack_port_type_id.restype = jack_port_type_id_t

jlib.jack_port_is_mine.argtypes = [POINTER(jack_client_t), POINTER(jack_port_t)]
jlib.jack_port_is_mine.restype = c_int

jlib.jack_port_connected.argtypes = [POINTER(jack_port_t)]
jlib.jack_port_connected.restype = c_int

jlib.jack_port_connected_to.argtypes = [POINTER(jack_port_t), c_char_p]
jlib.jack_port_connected_to.restype = c_int

jlib.jack_port_get_connections.argtypes = [POINTER(jack_port_t)]
jlib.jack_port_get_connections.restype = POINTER(c_char_p)

jlib.jack_port_get_all_connections.argtypes = [POINTER(jack_client_t), POINTER(jack_port_t)]
jlib.jack_port_get_all_connections.restype = POINTER(c_char_p)

jlib.jack_port_tie.argtypes = [POINTER(jack_port_t), POINTER(jack_port_t)]
jlib.jack_port_tie.restype = c_int

jlib.jack_port_untie.argtypes = [POINTER(jack_port_t)]
jlib.jack_port_untie.restype = c_int

jlib.jack_port_set_name.argtypes = [POINTER(jack_port_t), c_char_p]
jlib.jack_port_set_name.restype = c_int

jlib.jack_port_set_alias.argtypes = [POINTER(jack_port_t), c_char_p]
jlib.jack_port_set_alias.restype = c_int

jlib.jack_port_unset_alias.argtypes = [POINTER(jack_port_t), c_char_p]
jlib.jack_port_unset_alias.restype = c_int

jlib.jack_port_get_aliases.argtypes = [POINTER(jack_port_t), POINTER(ARRAY(c_char_p, 2))]
jlib.jack_port_get_aliases.restype = c_int

jlib.jack_port_request_monitor.argtypes = [POINTER(jack_port_t), c_int]
jlib.jack_port_request_monitor.restype = c_int

jlib.jack_port_request_monitor_by_name.argtypes = [POINTER(jack_client_t), c_char_p, c_int]
jlib.jack_port_request_monitor_by_name.restype = c_int

jlib.jack_port_ensure_monitor.argtypes = [POINTER(jack_port_t), c_int]
jlib.jack_port_ensure_monitor.restype = c_int

jlib.jack_port_monitoring_input.argtypes = [POINTER(jack_port_t)]
jlib.jack_port_monitoring_input.restype = c_int

jlib.jack_connect.argtypes = [POINTER(jack_client_t), c_char_p, c_char_p]
jlib.jack_connect.restype = c_int

jlib.jack_disconnect.argtypes = [POINTER(jack_client_t), c_char_p, c_char_p]
jlib.jack_disconnect.restype = c_int

jlib.jack_port_disconnect.argtypes = [POINTER(jack_client_t), POINTER(jack_port_t)]
jlib.jack_port_disconnect.restype = c_int

jlib.jack_port_name_size.argtypes = None
jlib.jack_port_name_size.restype = c_int

jlib.jack_port_type_size.argtypes = None
jlib.jack_port_type_size.restype = c_int

# JACK1 >= 0.125.0, JACK2 >= 1.19.11
try:
    jlib.jack_port_rename.argtypes = [POINTER(jack_client_t), POINTER(jack_port_t), c_char_p]
    jlib.jack_port_rename.restype = c_int
except AttributeError:
    jlib.jack_port_rename = None

try:
    jlib.jack_port_type_get_buffer_size.argtypes = [POINTER(jack_client_t), c_char_p]
    jlib.jack_port_type_get_buffer_size.restype = c_size_t
except AttributeError:
    jlib.jack_port_type_get_buffer_size = None

try:
    jlib.jack_port_uuid.argtypes = [POINTER(jack_port_t)]
    jlib.jack_port_uuid.restype = jack_uuid_t
except AttributeError:
    jlib.jack_port_uuid = None


def port_register(client, port_name, port_type, flags, buffer_size):
    return jlib.jack_port_register(client, _e(port_name), _e(port_type), flags, buffer_size)


def port_unregister(client, port):
    return jlib.jack_port_unregister(client, port)


def port_get_buffer(port, nframes):
    return jlib.jack_port_get_buffer(port, nframes)


def port_name(port) -> str:
    return _d(jlib.jack_port_name(port))


def port_short_name(port) -> str:
    return _d(jlib.jack_port_short_name(port))


def port_flags(port) -> int:
    return jlib.jack_port_flags(port)


def port_type(port) -> str:
    return _d(jlib.jack_port_type(port))


# JACK2 only:
def port_type_id(port):
    return jlib.jack_port_type_id(port)


def port_is_mine(client, port):
    return jlib.jack_port_is_mine(client, port)


def port_connected(port):
    return jlib.jack_port_connected(port)


def port_connected_to(port, port_name):
    return jlib.jack_port_connected_to(port, _e(port_name))


def port_get_connections(port) -> Iterator[str]:
    ports = jlib.jack_port_get_connections(port)
    if not ports:
        return
    for port_name in ports:
        if port_name is None:
            break
        yield _d(port_name)


def port_get_all_connections(client, port) -> Iterator[str]:
    ports = jlib.jack_port_get_all_connections(client, port)
    if not ports:
        return
    for port_name in ports:
        if port_name is None:
            break
        yield _d(port_name)


def port_tie(src, dst):
    return jlib.jack_port_tie(src, dst)


def port_untie(port):
    return jlib.jack_port_untie(port)


def port_set_name(port, port_name: str):
    return jlib.jack_port_set_name(port, _e(port_name))


# JACK1 >= 0.125.0, JACK2 >= 1.19.11
def port_rename(client, port, port_name: str):
    if jlib.jack_port_rename:
        return jlib.jack_port_rename(client, port, _e(port_name))

    return -1


def port_set_alias(port, alias):
    return jlib.jack_port_set_alias(port, _e(alias))


def port_unset_alias(port, alias):
    return jlib.jack_port_unset_alias(port, _e(alias))


def port_get_aliases(port):
    # NOTE - this function has no 2nd argument in jacklib
    # Instead, aliases will be passed in return value, in form of (int ret, str alias1, str alias2)
    name_size = port_name_size()
    alias_type = c_char_p * 2
    aliases = alias_type(b" " * name_size, b" " * name_size)
    ret = jlib.jack_port_get_aliases(port, pointer(aliases))
    return ret, _d(aliases[0]), _d(aliases[1])


def port_request_monitor(port, onoff):
    return jlib.jack_port_request_monitor(port, onoff)


def port_request_monitor_by_name(client, port_name, onoff):
    return jlib.jack_port_request_monitor_by_name(client, _e(port_name), onoff)


def port_ensure_monitor(port, onoff):
    return jlib.jack_port_ensure_monitor(port, onoff)


def port_monitoring_input(port):
    return jlib.jack_port_monitoring_input(port)


def connect(client, source_port: str, destination_port: str):
    return jlib.jack_connect(client, _e(source_port), _e(destination_port))


def disconnect(client, source_port: str, destination_port: str):
    return jlib.jack_disconnect(client, _e(source_port), _e(destination_port))


def port_disconnect(client, port):
    return jlib.jack_port_disconnect(client, port)


def port_name_size():
    return jlib.jack_port_name_size()


def port_type_size():
    return jlib.jack_port_type_size()


def port_type_get_buffer_size(client, port_type):
    if jlib.jack_port_type_get_buffer_size:
        return jlib.jack_port_type_get_buffer_size(client, _e(port_type))

    return 0


def port_uuid(port):
    if jlib.jack_port_uuid:
        return jlib.jack_port_uuid(port)

    return -1


# -------------------------------------------------------------------------------------------------
# Latency Functions

jlib.jack_port_set_latency.argtypes = [POINTER(jack_port_t), jack_nframes_t]
jlib.jack_port_set_latency.restype = None

try:
    jlib.jack_port_get_latency_range.argtypes = [
        POINTER(jack_port_t),
        jack_latency_callback_mode_t,
        POINTER(jack_latency_range_t),
    ]
    jlib.jack_port_get_latency_range.restype = None
except AttributeError:
    jlib.jack_port_get_latency_range = None

try:
    jlib.jack_port_set_latency_range.argtypes = [
        POINTER(jack_port_t),
        jack_latency_callback_mode_t,
        POINTER(jack_latency_range_t),
    ]
    jlib.jack_port_set_latency_range.restype = None
except AttributeError:
    jlib.jack_port_set_latency_range = None

jlib.jack_recompute_total_latencies.argtypes = [POINTER(jack_client_t)]
jlib.jack_recompute_total_latencies.restype = c_int

jlib.jack_port_get_latency.argtypes = [POINTER(jack_port_t)]
jlib.jack_port_get_latency.restype = jack_nframes_t

jlib.jack_port_get_total_latency.argtypes = [POINTER(jack_client_t), POINTER(jack_port_t)]
jlib.jack_port_get_total_latency.restype = jack_nframes_t

jlib.jack_recompute_total_latency.argtypes = [POINTER(jack_client_t), POINTER(jack_port_t)]
jlib.jack_recompute_total_latency.restype = c_int


def port_set_latency(port, nframes):
    jlib.jack_port_set_latency(port, nframes)


def port_get_latency_range(port, mode, range_):
    if jlib.jack_port_get_latency_range:
        jlib.jack_port_get_latency_range(port, mode, range_)


def port_set_latency_range(port, mode, range_):
    if jlib.jack_port_set_latency_range:
        jlib.jack_port_set_latency_range(port, mode, range_)


def recompute_total_latencies():
    return jlib.jack_recompute_total_latencies()


def port_get_latency(port):
    return jlib.jack_port_get_latency(port)


def port_get_total_latency(client, port):
    return jlib.jack_port_get_total_latency(client, port)


def recompute_total_latency(client, port):
    return jlib.jack_recompute_total_latency(client, port)


# -------------------------------------------------------------------------------------------------
# Port Searching

jlib.jack_get_ports.argtypes = [POINTER(jack_client_t), c_char_p, c_char_p, c_ulong]
jlib.jack_get_ports.restype = POINTER(c_char_p)

jlib.jack_port_by_name.argtypes = [POINTER(jack_client_t), c_char_p]
jlib.jack_port_by_name.restype = POINTER(jack_port_t)

jlib.jack_port_by_id.argtypes = [POINTER(jack_client_t), jack_port_id_t]
jlib.jack_port_by_id.restype = POINTER(jack_port_t)


def get_ports(client, port_name_pattern=None,
              type_name_pattern=None, flags=0) -> 'pointer[c_char_p]':
    return jlib.jack_get_ports(
        client, _e(port_name_pattern or ""), _e(type_name_pattern or ""), flags
    )


def port_by_name(client, port_name: str) -> 'pointer[jack_port_t]':
    return jlib.jack_port_by_name(client, _e(port_name))


def port_by_id(client, port_id) -> 'pointer[jack_port_t]':
    return jlib.jack_port_by_id(client, port_id)


# -------------------------------------------------------------------------------------------------
# Time Functions

jlib.jack_frames_since_cycle_start.argtypes = [POINTER(jack_client_t)]
jlib.jack_frames_since_cycle_start.restype = jack_nframes_t

jlib.jack_frame_time.argtypes = [POINTER(jack_client_t)]
jlib.jack_frame_time.restype = jack_nframes_t

jlib.jack_last_frame_time.argtypes = [POINTER(jack_client_t)]
jlib.jack_last_frame_time.restype = jack_nframes_t

try:
    # JACK_OPTIONAL_WEAK_EXPORT
    jlib.jack_get_cycle_times.argtypes = [
        POINTER(jack_client_t),
        POINTER(jack_nframes_t),
        POINTER(jack_time_t),
        POINTER(jack_time_t),
        POINTER(c_float),
    ]
    jlib.jack_get_cycle_times.restype = c_int
except AttributeError:
    jlib.jack_get_cycle_times = None

jlib.jack_frames_to_time.argtypes = [POINTER(jack_client_t), jack_nframes_t]
jlib.jack_frames_to_time.restype = jack_time_t

jlib.jack_time_to_frames.argtypes = [POINTER(jack_client_t), jack_time_t]
jlib.jack_time_to_frames.restype = jack_nframes_t

jlib.jack_get_time.argtypes = None
jlib.jack_get_time.restype = jack_time_t


def frames_since_cycle_start(client):
    return jlib.jack_frames_since_cycle_start(client)


def frame_time(client):
    return jlib.jack_frame_time(client)


def last_frame_time(client):
    return jlib.jack_last_frame_time(client)


def get_cycle_times(client, current_frames, current_usecs, next_usecs, period_usecs):
    # JACK_OPTIONAL_WEAK_EXPORT
    if jlib.jack_frames_to_time:
        return jlib.jack_get_cycle_times(
            client, current_frames, current_usecs, next_usecs, period_usecs
        )
    return -1


def frames_to_time(client, nframes):
    return jlib.jack_frames_to_time(client, nframes)


def time_to_frames(client, time):
    return jlib.jack_time_to_frames(client, time)


def get_time():
    return jlib.jack_get_time()


# -------------------------------------------------------------------------------------------------
# Error Output

# TODO

# -------------------------------------------------------------------------------------------------
# Misc

_error_callback = None

jlib.jack_free.argtypes = [c_void_p]
jlib.jack_free.restype = None

try:
    jlib.jack_set_error_function.argtypes = [JackErrorCallback]
    jlib.jack_set_error_function.restype = None
except AttributeError:
    jlib.jack_set_error_function = None


def set_error_function(error_callback):
    global _error_callback
    if jlib.jack_set_error_function:
        _error_callback = JackErrorCallback(error_callback)
        jlib.jack_set_error_function(_error_callback)


def free(ptr):
    return jlib.jack_free(ptr)


# -------------------------------------------------------------------------------------------------
# Transport

_sync_callback = _timebase_callback = None

jlib.jack_release_timebase.argtypes = [POINTER(jack_client_t)]
jlib.jack_release_timebase.restype = c_int

# jlib.jack_set_sync_callback.argtypes = [POINTER(jack_client_t), JackSyncCallback, c_void_p]
# jlib.jack_set_sync_callback.restype = c_int

jlib.jack_set_sync_timeout.argtypes = [POINTER(jack_client_t), jack_time_t]
jlib.jack_set_sync_timeout.restype = c_int

jlib.jack_set_timebase_callback.argtypes = [
    POINTER(jack_client_t),
    c_int,
    JackTimebaseCallback,
    c_void_p,
]
jlib.jack_set_timebase_callback.restype = c_int

jlib.jack_transport_locate.argtypes = [POINTER(jack_client_t), jack_nframes_t]
jlib.jack_transport_locate.restype = c_int

jlib.jack_transport_query.argtypes = [POINTER(jack_client_t), POINTER(jack_position_t)]
jlib.jack_transport_query.restype = jack_transport_state_t

jlib.jack_get_current_transport_frame.argtypes = [POINTER(jack_client_t)]
jlib.jack_get_current_transport_frame.restype = jack_nframes_t

jlib.jack_transport_reposition.argtypes = [POINTER(jack_client_t), POINTER(jack_position_t)]
jlib.jack_transport_reposition.restype = c_int

jlib.jack_transport_start.argtypes = [POINTER(jack_client_t)]
jlib.jack_transport_start.restype = None

jlib.jack_transport_stop.argtypes = [POINTER(jack_client_t)]
jlib.jack_transport_stop.restype = None


def release_timebase(client):
    return jlib.jack_release_timebase(client)

@callback_setter
def set_sync_callback(client, sync_callback, arg):
    ...

def set_sync_timeout(client, timeout):
    return jlib.jack_set_sync_timeout(client, timeout)


def set_timebase_callback(client, conditional, timebase_callback, arg):
    global _timebase_callback
    _timebase_callback = JackTimebaseCallback(timebase_callback)
    return jlib.jack_set_timebase_callback(client, conditional, _timebase_callback, arg)


def transport_locate(client, frame):
    return jlib.jack_transport_locate(client, frame)


def transport_query(client, pos):
    return jlib.jack_transport_query(client, pos)


def get_current_transport_frame(client):
    return jlib.jack_get_current_transport_frame(client)


def transport_reposition(client, pos):
    return jlib.jack_transport_reposition(client, pos)


def transport_start(client):
    return jlib.jack_transport_start(client)


def transport_stop(client):
    return jlib.jack_transport_stop(client)


# -------------------------------------------------------------------------------------------------
# MIDI

jlib.jack_midi_get_event_count.argtypes = [c_void_p]
jlib.jack_midi_get_event_count.restype = jack_nframes_t

jlib.jack_midi_event_get.argtypes = [POINTER(jack_midi_event_t), c_void_p, c_uint32]
jlib.jack_midi_event_get.restype = c_int

jlib.jack_midi_clear_buffer.argtypes = [c_void_p]
jlib.jack_midi_clear_buffer.restype = None

jlib.jack_midi_max_event_size.argtypes = [c_void_p]
jlib.jack_midi_max_event_size.restype = c_size_t

jlib.jack_midi_event_reserve.argtypes = [c_void_p, jack_nframes_t, c_size_t]
jlib.jack_midi_event_reserve.restype = POINTER(jack_midi_data_t)

jlib.jack_midi_event_write.argtypes = [
    c_void_p,
    jack_nframes_t,
    POINTER(jack_midi_data_t),
    c_size_t,
]
jlib.jack_midi_event_write.restype = c_int

jlib.jack_midi_get_lost_event_count.argtypes = [c_void_p]
jlib.jack_midi_get_lost_event_count.restype = c_uint32


def midi_get_event_count(port_buffer):
    return jlib.jack_midi_get_event_count(port_buffer)


def midi_event_get(event, port_buffer, event_index):
    return jlib.jack_midi_event_get(event, port_buffer, event_index)


def midi_clear_buffer(port_buffer):
    return jlib.jack_midi_clear_buffer(port_buffer)


def midi_max_event_size(port_buffer):
    return jlib.jack_midi_max_event_size(port_buffer)


def midi_event_reserve(port_buffer, time, data_size):
    return jlib.jack_midi_event_reserve(port_buffer, time, data_size)


def midi_event_write(port_buffer, time, data, data_size):
    return jlib.jack_midi_event_write(port_buffer, time, data, data_size)


def midi_get_lost_event_count(port_buffer):
    return jlib.jack_midi_get_lost_event_count(port_buffer)


# -------------------------------------------------------------------------------------------------
# Session

try:
    jlib.jack_session_reply.argtypes = [POINTER(jack_client_t), POINTER(jack_session_event_t)]
    jlib.jack_session_reply.restype = c_int
except AttributeError:
    jlib.jack_session_reply = None

try:
    jlib.jack_session_event_free.argtypes = [POINTER(jack_session_event_t)]
    jlib.jack_session_event_free.restype = None
except AttributeError:
    jlib.jack_session_event_free = None

try:
    jlib.jack_client_get_uuid.argtypes = [POINTER(jack_client_t)]
    jlib.jack_client_get_uuid.restype = c_char_p
except AttributeError:
    jlib.jack_client_get_uuid = None

try:
    jlib.jack_session_notify.argtypes = [
        POINTER(jack_client_t),
        c_char_p,
        jack_session_event_type_t,
        c_char_p,
    ]
    jlib.jack_session_notify.restype = POINTER(jack_session_command_t)
except AttributeError:
    jlib.jack_session_notify = None

try:
    jlib.jack_session_commands_free.argtypes = [POINTER(jack_session_command_t)]
    jlib.jack_session_commands_free.restype = None
except AttributeError:
    jlib.jack_session_commands_free = None

try:
    jlib.jack_get_uuid_for_client_name.argtypes = [POINTER(jack_client_t), c_char_p]
    jlib.jack_get_uuid_for_client_name.restype = c_char_p
except AttributeError:
    jlib.jack_get_uuid_for_client_name = None

try:
    jlib.jack_get_client_name_by_uuid.argtypes = [POINTER(jack_client_t), c_char_p]
    jlib.jack_get_client_name_by_uuid.restype = c_char_p
except AttributeError:
    jlib.jack_get_client_name_by_uuid = None

try:
    jlib.jack_reserve_client_name.argtypes = [POINTER(jack_client_t), c_char_p, c_char_p]
    jlib.jack_reserve_client_name.restype = c_int
except AttributeError:
    jlib.jack_reserve_client_name = None

try:
    jlib.jack_client_has_session_callback.argtypes = [POINTER(jack_client_t), c_char_p]
    jlib.jack_client_has_session_callback.restype = c_int
except AttributeError:
    jlib.jack_client_has_session_callback = None

try:
    jlib.jack_uuid_parse.argtypes = [c_char_p, POINTER(jack_uuid_t)]
    jlib.jack_uuid_parse.restype = c_int
except AttributeError:
    jlib.jack_uuid_parse = None

try:
    jlib.jack_uuid_unparse.argtypes = [jack_uuid_t, c_char_p]
    jlib.jack_uuid_unparse.restype = None
except AttributeError:
    jlib.jack_uuid_unparse = None

@callback_setter
def set_session_callback(client, session_callback, arg):
    ...

def session_reply(client, event):
    if jlib.jack_session_reply:
        return jlib.jack_session_reply(client, event)

    return -1


def session_event_free(event):
    if jlib.jack_session_event_free:
        jlib.jack_session_event_free(event)


def client_get_uuid(client):
    if jlib.jack_client_get_uuid:
        return _d(jlib.jack_client_get_uuid(client))

    return None


def session_notify(client, target, type_, path):
    if jlib.jack_session_notify:
        return jlib.jack_session_notify(client, _e(target), type_, _e(path))

    return jack_session_command_t()


def session_commands_free(cmds):
    if jlib.jack_session_commands_free:
        jlib.jack_session_commands_free(cmds)


def get_uuid_for_client_name(client, client_name):
    if jlib.jack_get_uuid_for_client_name:
        return jlib.jack_get_uuid_for_client_name(client, _e(client_name))

    return None


def get_client_name_by_uuid(client, client_uuid):
    if jlib.jack_get_client_name_by_uuid:
        return jlib.jack_get_client_name_by_uuid(client, _e(client_uuid))

    return None


def reserve_client_name(client, name, uuid):
    if jlib.jack_reserve_client_name:
        return jlib.jack_reserve_client_name(client, _e(name), _e(uuid))

    return -1


def client_has_session_callback(client, client_name):
    if jlib.jack_client_has_session_callback:
        return jlib.jack_client_has_session_callback(client, _e(client_name))

    return -1


def uuid_parse(uuid_cstr):
    if jlib.jack_uuid_parse and uuid_cstr is not None:
        uuid = jack_uuid_t()
        res = jlib.jack_uuid_parse(uuid_cstr, byref(uuid))
        return uuid if res != -1 else None

    return -1


def uuid_unparse(uuid, encoding=ENCODING):
    if jlib.jack_uuid_unparse:
        uuid_str = c_char_p(b" " * JACK_UUID_STRING_SIZE)
        jlib.jack_uuid_unparse(uuid, uuid_str)
        return _d(uuid_str.value, encoding)

    return ""


# -------------------------------------------------------------------------------------------------
# Meta data

Property = namedtuple("Property", ("key", "value", "type"))

try:
    jlib.jack_free_description.argtypes = [POINTER(jack_description_t), c_int]
    jlib.jack_free_description.restype = None

    jlib.jack_get_all_properties.argtypes = [POINTER(POINTER(jack_description_t))]
    jlib.jack_get_all_properties.restype = c_int

    jlib.jack_get_properties.argtypes = [jack_uuid_t, POINTER(jack_description_t)]
    jlib.jack_get_properties.restype = c_int

    jlib.jack_get_property.argtypes = [jack_uuid_t, c_char_p, POINTER(c_char_p), POINTER(c_char_p)]
    jlib.jack_get_property.restype = c_int

    jlib.jack_remove_all_properties.argtypes = [POINTER(jack_client_t)]
    jlib.jack_remove_all_properties.restype = c_int

    jlib.jack_remove_properties.argtypess = [POINTER(jack_client_t), POINTER(jack_uuid_t)]
    jlib.jack_remove_properties.restype = c_int

    jlib.jack_remove_property.argtypes = [POINTER(jack_client_t), POINTER(jack_uuid_t), c_char_p]
    jlib.jack_remove_property.restype = c_int

    jlib.jack_set_property.argtypes = [
        POINTER(jack_client_t),
        jack_uuid_t,
        c_char_p,
        c_char_p,
        c_char_p,
    ]
    jlib.jack_set_property.restype = c_int

except AttributeError:
    jlib.jack_free_description = None
    jlib.jack_get_properties = None
    jlib.jack_get_property = None
    jlib.jack_remove_all_properties = None
    jlib.jack_remove_properties = None
    jlib.jack_remove_property = None
    jlib.jack_set_property = None


def free_description(description, free_description_itself=0):
    if jlib.jack_free_description:
        jlib.jack_free_description(description, free_description_itself)


def _decode_property(prop, encoding=ENCODING):
    key, value, type_ = prop.key, prop.data, prop.type
    decode_value = True

    try:
        key = _d(key, encoding)
    except UnicodeDecodeError:
        pass

    if type_:
        try:
            type_ = _d(type_, encoding)
        except UnicodeDecodeError:
            pass
        else:
            decode_value = type_.startswith("text/")

    if decode_value:
        try:
            value = _d(value, encoding)
        except UnicodeDecodeError:
            pass

    return Property(key, value, type_)


def get_all_properties(encoding=ENCODING):
    descriptions = POINTER(jack_description_t)()
    ret = jlib.jack_get_all_properties(byref(descriptions))
    results = {}

    if ret != -1:
        for p_idx in range(ret):
            description = descriptions[p_idx]

            if description.property_cnt:
                results[description.subject] = [
                    _decode_property(description.properties[p_idx], encoding)
                    for p_idx in range(description.property_cnt)
                ]

            free_description(description, 0)

    free(descriptions)
    return results


def get_properties(subject, encoding=ENCODING):
    description = jack_description_t()
    ret = jlib.jack_get_properties(subject, byref(description))
    results = []

    if ret != -1:
        for p_idx in range(description.property_cnt):
            results.append(_decode_property(description.properties[p_idx], encoding))

    free_description(byref(description), 0)
    return results


def get_client_properties(client, client_uuid, encoding=ENCODING):
    if isinstance(client_uuid, str):
        client_uuid = get_uuid_for_client_name(client, client_uuid)

    return get_properties(uuid_parse(client_uuid), encoding)


def get_port_properties(client, port, encoding=ENCODING):
    if not isinstance(port, POINTER(jack_port_t)):
        port = port_by_name(client, port)

    return get_properties(port_uuid(port), encoding)


def get_property(subject, key, encoding=ENCODING):
    # FIXME: how to handle non-null terminated data in value?
    #        We wouldn't know the length of the data in the value buffer.
    #        This seems to be an oversight in the JACK meta data API.
    value_c = c_char_p()
    type_c = c_char_p()
    ret = jlib.jack_get_property(subject, _e(key), byref(value_c), byref(type_c))
    value = value_c.value

    if ret != -1:
        decode_value = True

        if type_c:
            try:
                type_ = _d(type_c.value, encoding)
            except UnicodeDecodeError:
                # If type can't be decoded, we assume it's neither a mimetype
                # nor a URI, so we don't know how to interpret it and won't use
                # it to decide whether to decode the property value.
                type_ = type_c.value
            else:
                decode_value = type_.startswith("text/")

            free(type_c)
        else:
            type_ = None

        if decode_value:
            try:
                value = _d(value_c.value, encoding)
            except UnicodeDecodeError:
                pass

        free(value_c)
        return Property(key, value, type_)


def get_client_property(client, client_uuid, key, encoding=ENCODING):
    if isinstance(client_uuid, str):
        client_uuid = get_uuid_for_client_name(client, client_uuid)

    return get_property(uuid_parse(client_uuid), key, encoding)


def get_port_property(client, port, key, encoding=ENCODING):
    if not isinstance(port, POINTER(jack_port_t)):
        port = port_by_name(client, port)

    return get_property(port_uuid(port), key, encoding)


def get_port_pretty_name(client, port, encoding=ENCODING):
    prop = get_port_property(client, port, JACK_METADATA_PRETTY_NAME, encoding)
    return prop.value if prop else None


def remove_all_properties(client):
    return jlib.jack_remove_property(client)


def remove_properties(client, subject):
    return jlib.jack_remove_property(client, subject)


def remove_client_properties(client, client_uuid):
    if isinstance(client_uuid, str):
        client_uuid = get_uuid_for_client_name(client, client_uuid)

    return remove_properties(client, uuid_parse(client_uuid))


def remove_port_properties(client, port):
    if not isinstance(port, POINTER(jack_port_t)):
        port = port_by_name(client, port)

    return remove_properties(client, port_uuid(port))


def remove_property(client, subject, key, encoding=ENCODING):
    return jlib.jack_remove_property(client, subject, _e(key, encoding))


def remove_client_property(client, client_uuid, key, encoding=ENCODING):
    if isinstance(client_uuid, str):
        client_uuid = get_uuid_for_client_name(client, client_uuid)

    return remove_property(client, uuid_parse(client_uuid), key, encoding)


def remove_port_property(client, port, key, encoding=ENCODING):
    if not isinstance(port, POINTER(jack_port_t)):
        port = port_by_name(client, port)

    return remove_property(client, port_uuid(port), key, encoding)


def set_property(client, subject, key, value, type=None, encoding=ENCODING):
    if value is not None and encoding:
        value = _e(value, encoding)

    if type is not None and encoding:
        type = _e(type, encoding)

    return jlib.jack_set_property(client, subject, _e(key, encoding), value, type)


def set_client_property(client, client_uuid, key, value, type=None, encoding=ENCODING):
    if isinstance(client_uuid, str):
        client_uuid = get_uuid_for_client_name(client, client_uuid)

    uuid = uuid_parse(client_uuid)
    return set_property(client, uuid, key, value, type, encoding) if uuid != -1 else -1


def set_port_property(client, port, key, value, type=None, encoding=ENCODING):
    if not isinstance(port, POINTER(jack_port_t)):
        port = port_by_name(client, port)

    uuid = port_uuid(port)
    return set_property(client, uuid, key, value, type, encoding) if uuid != -1 else -1


def set_port_pretty_name(client, port, value, encoding=ENCODING):
    return set_port_property(client, port, JACK_METADATA_PRETTY_NAME, value, "text/plain", encoding)

@callback_setter
def set_property_change_callback(client, callback, arg=None):
    ...