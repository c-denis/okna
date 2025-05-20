import multiprocessing

bind = 'unix:/tmp/crm.sock'
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'gunicorn.workers.gthread.ThreadWorker'
threads = 3
max_requests = 1000
max_requests_jitter = 50
timeout = 30
keepalive = 5
errorlog = '-'
loglevel = 'info'
accesslog = '-'