import sys
import pytest

import jacklib
from jacklib.helpers import get_jack_status_error_string

@pytest.fixture
def jack_client():
    status = jacklib.jack_status_t()
    client = jacklib.client_open("pyjacklib", jacklib.JackOptions.NO_START_SERVER, status)

    if status.value:
        err = get_jack_status_error_string(status)

        if status.value & jacklib.JackStatus.NAME_NOT_UNIQUE:
            print(f"Non-fatal JACK status: {err}", file=sys.stderr)
        elif status.value & jacklib.JackStatus.SERVER_STARTED:
            # Should not happen, since we use the JackOptions.NO_START_SERVER option
            print(f"Unexpected JACK status: {err}", file=sys.stderr)
        else:
            raise OSError(f"Error creating JACK client: {err}")

    yield client

    jacklib.client_close(client)
