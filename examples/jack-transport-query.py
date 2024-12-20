#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from ctypes import pointer
import jacklib
from jacklib import JackTransportState
from jacklib.helpers import get_jack_status_error_string


status = jacklib.jack_status_t()
client = jacklib.client_open(
    "transport-query", jacklib.JackOptions.NO_START_SERVER, status)
err = get_jack_status_error_string(status)

if status.value:
    if status.value & jacklib.JackStatus.NAME_NOT_UNIQUE:
        print("Non-fatal JACK status: %s" % err, file=sys.stderr)
    elif status.value & jacklib.JackStatus.SERVER_STARTED:
        # Should not happen, since we use the JackOptions.NO_START_SERVER option
        print("Unexpected JACK status: %s" % err, file=sys.stderr)
    else:
        sys.exit("Error connecting to JACK server: %s" % err)

position = jacklib.jack_position_t()
transport_state = jacklib.transport_query(client, pointer(position))

for name, type_ in sorted(position._fields_):
    value = getattr(position, name)
    if name == 'padding':
        value = list(value)
    print("{}: {}".format(name, value), file=sys.stderr)

if transport_state == JackTransportState.STOPPED:
    print("JACK transport stopped, starting it now.")
    jacklib.transport_start(client)
elif transport_state == JackTransportState.ROLLING:
    print("JACK transport rolling, stopping it now.")
    jacklib.transport_stop(client)
elif transport_state == JackTransportState.STARTING:
    print("JACK transport starting, nothing to do.")
else:
    print("Unknown JACK transport state.")

jacklib.client_close(client)
