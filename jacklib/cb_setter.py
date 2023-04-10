from typing import Callable
from ctypes import (
    CFUNCTYPE,
    POINTER,
    c_void_p,
    c_int,
    c_char_p,
    CDLL
)

from .types import (
    jack_client_t,
    jack_status_t,
    jack_nframes_t,
    jack_port_id_t,
    jack_latency_callback_mode_t,
    jack_transport_state_t,
    jack_position_t,
    jack_session_event_t,
    jack_uuid_t,
    jack_property_change_t
)


class _Cb:
    def __init__(self, ref: str, callback: CFUNCTYPE, restype, suffix='_callback'):
        self.ref = ref
        self.callback = callback
        self.restype = restype
        self.setter_name = ref + suffix
        try:
            func = getattr(globals()['_jlib'], 'jack_' + self.setter_name)
            func.argstypes = [POINTER(jack_client_t), self.callback, c_void_p]
            func.restype = self.restype
            self.jlib_func = func
        except AttributeError:
            self.jlib_func = None


_used_callbacks = list[CFUNCTYPE]()
_jlib = None
_cbs = tuple[_Cb]()

def init_callback_setter(jlib: CDLL):
    global _jlib, _cbs
    _jlib = jlib
    _cbs = (
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
    for _cb in _cbs:
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