#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import jacklib
from jacklib.helpers import get_jack_status_error_string


if sys.argv[1:]:
    portname = sys.argv[1]
else:
    sys.exit("Usage: %s <port name>" % sys.argv[0])

status = jacklib.jack_status_t()
client = jacklib.client_open("print-port-pretty-name", jacklib.JackOptions.NO_START_SERVER, status)
err = get_jack_status_error_string(status)

if status.value:
    if status.value & jacklib.JackStatus.NAME_NOT_UNIQUE:
        print("Non-fatal JACK status: %s" % err, file=sys.stderr)
    elif status.value & jacklib.JackStatus.SERVER_STARTED:
        # Should not happen, since we use the JackOptions.NO_START_SERVER option
        print("Unexpected JACK status: %s" % err, file=sys.stderr)
    else:
        sys.exit("Error connecting to JACK server: %s" % err)

pretty_name = jacklib.get_port_pretty_name(client, portname)
print("Pretty name for '%s': %r" % (portname, pretty_name or '<not set>'))

jacklib.client_close(client)
