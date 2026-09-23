"""
Configuració Gunicorn per Adabida
"""
import multiprocessing

# Servidor
bind = "127.0.0.1:5000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
timeout = 120

# Logging
accesslog = "/var/log/adabida/access.log"
errorlog = "/var/log/adabida/error.log"
loglevel = "info"

# Seguretat
limit_request_line = 4094
limit_request_fields = 100
