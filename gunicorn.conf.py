# gunicorn.conf.py
import os

# Worker configuration
def get_int_env(var_name, default):
    value = os.getenv(var_name, str(default))
    try:
        return int(value)
    except ValueError:
        raise RuntimeError(f"Invalid value for {var_name}: '{value}'. Must be an integer.")

workers = get_int_env("WORKERS", 1)
threads = get_int_env("THREADS", 2)
worker_class = "gthread"

# Bind configuration
bind = f"0.0.0.0:{int(os.getenv('PORT', 8080))}"

# Logging
accesslog = "-"
errorlog = "-"

# Timeout configuration
timeout = 300
keepalive = 5
