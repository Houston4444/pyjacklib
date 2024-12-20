#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import jacklib
from jacklib.helpers import get_jack_status_error_string


status = jacklib.jack_status_t()
client = jacklib.client_open("list-all-properties", jacklib.JackOptions.NO_START_SERVER, status)
err = get_jack_status_error_string(status)

if status.value:
    if status.value & jacklib.JackStatus.NAME_NOT_UNIQUE:
        print("Non-fatal JACK status: %s" % err, file=sys.stderr)
    elif status.value & jacklib.JackStatus.SERVER_STARTED:
        # Should not happen, since we use the JackOptions.NO_START_SERVER option
        print("Unexpected JACK status: %s" % err, file=sys.stderr)
    else:
        sys.exit("Error connecting to JACK server: %s" % err)

properties = jacklib.get_all_properties()

for subject, props in properties.items():
    print("Subject %s:" % subject)

    for prop in props:
        print("* {p.key}: {p.value} (type: {p.type})".format(p=prop))

    print('')

jacklib.client_close(client)
