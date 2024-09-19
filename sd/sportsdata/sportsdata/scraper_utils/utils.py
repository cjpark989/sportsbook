"""General purpose utilities."""
import time

import ipdb

sleep_one_sec = lambda: time.sleep(1)
time_ns = time.time_ns
set_trace = ipdb.set_trace
