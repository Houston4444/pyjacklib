"""Helper functions for extra jacklib functionality."""

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

from ctypes import pointer, c_char_p
from typing import Iterator
from . import api as jacklib
from .api import JackStatus


def get_jack_status_error_string(cStatus):
    """Get JACK error status as string."""

    status = cStatus.value

    if status == 0x0:
        return ""

    try:
        status = JackStatus(status)
    except:
        return ""

    error_string = list[str]()

    if status is JackStatus.FAILURE:
        # Only include this generic message if no other error status is set
        error_string.append("Overall operation failed")
    if status & JackStatus.INVALID_OPTION:
        error_string.append("The operation contained an invalid or unsupported option")
    if status & JackStatus.NAME_NOT_UNIQUE:
        error_string.append("The desired client name was not unique")
    if status & JackStatus.SERVER_STARTED:
        error_string.append("The JACK server was started as a result of this operation")
    if status & JackStatus.SERVER_FAILED:
        error_string.append("Unable to connect to the JACK server")
    if status & JackStatus.SERVER_ERROR:
        error_string.append("Communication error with the JACK server")
    if status & JackStatus.NO_SUCH_CLIENT:
        error_string.append("Requested client does not exist")
    if status & JackStatus.LOAD_FAILURE:
        error_string.append("Unable to load internal client")
    if status & JackStatus.INIT_FAILURE:
        error_string.append("Unable to initialize client")
    if status & JackStatus.SHM_FAILURE:
        error_string.append("Unable to access shared memory")
    if status & JackStatus.VERSION_ERROR:
        error_string.append("Client's protocol version does not match")
    if status & JackStatus.BACKEND_ERROR:
        error_string.append("Backend Error")
    if status & JackStatus.CLIENT_ZOMBIE:
        error_string.append("Client is being shutdown against its will")

    return ";\n".join(error_string) + "."


def c_char_p_p_to_list(c_char_p_p: 'pointer[c_char_p]',
                       encoding=jacklib.ENCODING,
                       errors="ignore") -> list[str]:
    """Convert C char** -> Python list of strings."""
    i = 0
    ret_list = list[str]()

    if not c_char_p_p:
        return ret_list

    while True:
        new_char_p = c_char_p_p[i]
        if not new_char_p:
            break

        ret_list.append(new_char_p.decode(encoding=encoding, errors=errors))
        i += 1

    jacklib.free(c_char_p_p)
    return ret_list


def iterate_c_char_p_p(c_char_p_p: 'pointer[c_char_p]',
                       encoding=jacklib.ENCODING,
                       errors="ignore") -> Iterator[str]:
    i = 0
    
    if not c_char_p:
        return
    
    while True:
        new_char_p = c_char_p_p[i]
        if not new_char_p:
            break
        
        yield new_char_p.decode(encoding=encoding, errors=errors)
        i += 1
        
    jacklib.free(c_char_p_p)


def voidptr2str(void_p) -> str:
    """Convert C void* -> string."""
    char_p = jacklib.cast(void_p, jacklib.c_char_p)
    string = str(char_p.value, encoding="utf-8")
    return string


def translate_audio_port_buffer(void_p):
    """Convert C void* -> jack_default_audio_sample_t*."""

    return jacklib.cast(void_p, jacklib.POINTER(jacklib.jack_default_audio_sample_t))


def translate_midi_event_buffer(void_p, size):
    """Convert a JACK MIDI buffer into a Python tuple of 0-4 elements."""

    if not void_p:
        return ()
    elif size == 1:
        return (void_p[0],)
    elif size == 2:
        return (void_p[0], void_p[1])
    elif size == 3:
        return (void_p[0], void_p[1], void_p[2])
    elif size == 4:
        return (void_p[0], void_p[1], void_p[2], void_p[3])
    else:
        return ()
