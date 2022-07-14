import os
import multiprocessing

timeout = os.getenv("wsgi_timeout") or 600
threads = os.getenv("wsgi_threads") or 10
loglevel = os.getenv("wsgi_loglevel") or ""
workers = multiprocessing.cpu_count()
bind = "0.0.0.0:5001"
