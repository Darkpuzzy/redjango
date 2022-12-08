import multiprocessing
import os
import threading
import logging

from django.core.wsgi import get_wsgi_application
from users.cashinfo import setup_logging, logger, check_ram
from helpers.server_check import check_ram_tcp


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'redapi.settings')

# LOGGIN INFO
setup_logging()
process_name = multiprocessing.current_process().name
logger.info(f'Process {process_name} started')
for k, v in os.environ.items():
    logger.info(f'{k}={v}')

logger.info("Server started")

thr = threading.Thread(target=check_ram, daemon=True).start()
another_thr = threading.Thread(target=check_ram_tcp, daemon=True).start()

application = get_wsgi_application()
