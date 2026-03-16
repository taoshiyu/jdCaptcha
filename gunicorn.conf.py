import multiprocessing

# binding = '0.0.0.0:5051'

# workers  = multiprocessing.cpu_count() * 2 + 1
workers = 1

preload_app = True

threads = 200

timeout = 30

loglevel = 'info'

daemon = False

keepalive = 20

graceful_timeout = 30

worker_class = 'gthread'

worker_connections = 1024
