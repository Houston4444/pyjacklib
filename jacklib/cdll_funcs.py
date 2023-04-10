from ctypes import (
    ARRAY,
    CDLL,
    c_char_p,
    POINTER,
    c_int,
    c_void_p,
    c_float,
    c_ulong,
    c_uint32,
    c_size_t)

from .types import (
    jack_client_t,
    jack_port_t,
    jack_port_id_t,
    jack_port_type_id_t,
    jack_options_t,
    jack_status_t,
    jack_nframes_t,
    jack_uuid_t,
    jack_time_t,
    jack_latency_callback_mode_t,
    jack_transport_state_t,
    jack_midi_data_t,
    jack_position_t,
    jack_midi_event_t,
    jack_latency_range_t,
    JackThreadCallback,
    JackErrorCallback,
    JackTimebaseCallback
)

_JACK2 = True

def set_jack2(yesno: bool):
    global _JACK2
    _JACK2 = yesno

def setup_cdll_functions(jlib: CDLL):
    try:
        jlib.jack_get_version_string.argtypes = None
        jlib.jack_get_version_string.restype = c_char_p
    except AttributeError:
        jlib.jack_get_version_string = None

    try:
        jlib.jack_client_open.argtypes = [
            c_char_p, jack_options_t, POINTER(jack_status_t), c_char_p]
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
        
def setup_non_callback_cdll_func(jlib: CDLL):
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
        jlib.jack_set_process_thread.argtypes = [
            POINTER(jack_client_t), JackThreadCallback, c_void_p]
        jlib.jack_set_process_thread.restype = c_int
    except AttributeError:
        jlib.jack_set_process_thread = None
        
def setup_server_control_funcs(jlib: CDLL):
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
    
def setup_port_funcs(jlib: CDLL):
    jlib.jack_port_register.argtypes = [
        POINTER(jack_client_t), c_char_p, c_char_p, c_ulong, c_ulong]
    jlib.jack_port_register.restype = POINTER(jack_port_t)

    jlib.jack_port_unregister.argtypes = [
        POINTER(jack_client_t), POINTER(jack_port_t)]
    jlib.jack_port_unregister.restype = c_int

    jlib.jack_port_get_buffer.argtypes = [
        POINTER(jack_port_t), jack_nframes_t]
    jlib.jack_port_get_buffer.restype = c_void_p

    jlib.jack_port_name.argtypes = [POINTER(jack_port_t)]
    jlib.jack_port_name.restype = c_char_p

    jlib.jack_port_short_name.argtypes = [POINTER(jack_port_t)]
    jlib.jack_port_short_name.restype = c_char_p

    jlib.jack_port_flags.argtypes = [POINTER(jack_port_t)]
    jlib.jack_port_flags.restype = c_int

    jlib.jack_port_type.argtypes = [POINTER(jack_port_t)]
    jlib.jack_port_type.restype = c_char_p

    if _JACK2:
        jlib.jack_port_type_id.argtypes = [POINTER(jack_port_t)]
        jlib.jack_port_type_id.restype = jack_port_type_id_t

    jlib.jack_port_is_mine.argtypes = [
        POINTER(jack_client_t), POINTER(jack_port_t)]
    jlib.jack_port_is_mine.restype = c_int

    jlib.jack_port_connected.argtypes = [POINTER(jack_port_t)]
    jlib.jack_port_connected.restype = c_int

    jlib.jack_port_connected_to.argtypes = [POINTER(jack_port_t), c_char_p]
    jlib.jack_port_connected_to.restype = c_int

    jlib.jack_port_get_connections.argtypes = [POINTER(jack_port_t)]
    jlib.jack_port_get_connections.restype = POINTER(c_char_p)

    jlib.jack_port_get_all_connections.argtypes = [
        POINTER(jack_client_t), POINTER(jack_port_t)]
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

    jlib.jack_port_get_aliases.argtypes = [
        POINTER(jack_port_t), POINTER(ARRAY(c_char_p, 2))]
    jlib.jack_port_get_aliases.restype = c_int

    jlib.jack_port_request_monitor.argtypes = [POINTER(jack_port_t), c_int]
    jlib.jack_port_request_monitor.restype = c_int

    jlib.jack_port_request_monitor_by_name.argtypes = [
        POINTER(jack_client_t), c_char_p, c_int]
    jlib.jack_port_request_monitor_by_name.restype = c_int

    jlib.jack_port_ensure_monitor.argtypes = [POINTER(jack_port_t), c_int]
    jlib.jack_port_ensure_monitor.restype = c_int

    jlib.jack_port_monitoring_input.argtypes = [POINTER(jack_port_t)]
    jlib.jack_port_monitoring_input.restype = c_int

    jlib.jack_connect.argtypes = [POINTER(jack_client_t), c_char_p, c_char_p]
    jlib.jack_connect.restype = c_int

    jlib.jack_disconnect.argtypes = [
        POINTER(jack_client_t), c_char_p, c_char_p]
    jlib.jack_disconnect.restype = c_int

    jlib.jack_port_disconnect.argtypes = [
        POINTER(jack_client_t), POINTER(jack_port_t)]
    jlib.jack_port_disconnect.restype = c_int

    jlib.jack_port_name_size.argtypes = None
    jlib.jack_port_name_size.restype = c_int

    jlib.jack_port_type_size.argtypes = None
    jlib.jack_port_type_size.restype = c_int

    # JACK1 >= 0.125.0, JACK2 >= 1.19.11
    try:
        jlib.jack_port_rename.argtypes = [
            POINTER(jack_client_t), POINTER(jack_port_t), c_char_p]
        jlib.jack_port_rename.restype = c_int
    except AttributeError:
        jlib.jack_port_rename = None

    try:
        jlib.jack_port_type_get_buffer_size.argtypes = [
            POINTER(jack_client_t), c_char_p]
        jlib.jack_port_type_get_buffer_size.restype = c_size_t
    except AttributeError:
        jlib.jack_port_type_get_buffer_size = None

    try:
        jlib.jack_port_uuid.argtypes = [POINTER(jack_port_t)]
        jlib.jack_port_uuid.restype = jack_uuid_t
    except AttributeError:
        jlib.jack_port_uuid = None
        
def setup_latency_func(jlib: CDLL):
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

    jlib.jack_port_get_total_latency.argtypes = [
        POINTER(jack_client_t), POINTER(jack_port_t)]
    jlib.jack_port_get_total_latency.restype = jack_nframes_t

    jlib.jack_recompute_total_latency.argtypes = [
        POINTER(jack_client_t), POINTER(jack_port_t)]
    jlib.jack_recompute_total_latency.restype = c_int
    
def setup_port_searching_func(jlib: CDLL):
    jlib.jack_get_ports.argtypes = [POINTER(jack_client_t), c_char_p, c_char_p, c_ulong]
    jlib.jack_get_ports.restype = POINTER(c_char_p)

    jlib.jack_port_by_name.argtypes = [POINTER(jack_client_t), c_char_p]
    jlib.jack_port_by_name.restype = POINTER(jack_port_t)

    jlib.jack_port_by_id.argtypes = [POINTER(jack_client_t), jack_port_id_t]
    jlib.jack_port_by_id.restype = POINTER(jack_port_t)
    
def setup_time_func(jlib: CDLL):
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
    
def setup_misc_func(jlib: CDLL):
    jlib.jack_free.argtypes = [c_void_p]
    jlib.jack_free.restype = None

    try:
        jlib.jack_set_error_function.argtypes = [JackErrorCallback]
        jlib.jack_set_error_function.restype = None
    except AttributeError:
        jlib.jack_set_error_function = None
        
def setup_transport_func(jlib: CDLL):
    jlib.jack_release_timebase.argtypes = [POINTER(jack_client_t)]
    jlib.jack_release_timebase.restype = c_int

    # jlib.jack_set_sync_callback.argtypes = [POINTER(jack_client_t), JackSyncCallback, c_void_p]
    # jlib.jack_set_sync_callback.restype = c_int

    jlib.jack_set_sync_timeout.argtypes = [
        POINTER(jack_client_t), jack_time_t]
    jlib.jack_set_sync_timeout.restype = c_int

    jlib.jack_set_timebase_callback.argtypes = [
        POINTER(jack_client_t),
        c_int,
        JackTimebaseCallback,
        c_void_p,
    ]
    jlib.jack_set_timebase_callback.restype = c_int

    jlib.jack_transport_locate.argtypes = [
        POINTER(jack_client_t), jack_nframes_t]
    jlib.jack_transport_locate.restype = c_int

    jlib.jack_transport_query.argtypes = [
        POINTER(jack_client_t), POINTER(jack_position_t)]
    jlib.jack_transport_query.restype = jack_transport_state_t

    jlib.jack_get_current_transport_frame.argtypes = [POINTER(jack_client_t)]
    jlib.jack_get_current_transport_frame.restype = jack_nframes_t

    jlib.jack_transport_reposition.argtypes = [
        POINTER(jack_client_t), POINTER(jack_position_t)]
    jlib.jack_transport_reposition.restype = c_int

    jlib.jack_transport_start.argtypes = [POINTER(jack_client_t)]
    jlib.jack_transport_start.restype = None

    jlib.jack_transport_stop.argtypes = [POINTER(jack_client_t)]
    jlib.jack_transport_stop.restype = None
    
def setup_midi_func(jlib: CDLL):
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