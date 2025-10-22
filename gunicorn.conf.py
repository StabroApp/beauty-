# gunicorn.conf.py
import os

# Worker configuration
workers = int(os.getenv("WORKERS", 1))
threads = int(os.getenv("THREADS", 2))
worker_class = "gthread"

# Bind configuration
bind = f"0.0.0.0:{int(os.getenv('PORT', 8080))}"

# Logging
accesslog = "-"
errorlog = "-"

# Timeout configuration
timeout = 300
keepalive = 5
